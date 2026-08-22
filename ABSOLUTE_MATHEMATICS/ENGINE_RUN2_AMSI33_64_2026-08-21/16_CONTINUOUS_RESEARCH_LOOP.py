from __future__ import annotations
import sqlite3, json, time, hashlib

SCHEMA="""
CREATE TABLE IF NOT EXISTS jobs(
 id TEXT PRIMARY KEY,
 payload TEXT NOT NULL,
 status TEXT NOT NULL,
 priority REAL NOT NULL,
 parent_id TEXT,
 attempts INTEGER NOT NULL DEFAULT 0,
 created REAL NOT NULL,
 updated REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS results(
 job_id TEXT PRIMARY KEY,
 result TEXT NOT NULL,
 result_sha256 TEXT NOT NULL,
 created REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS events(
 seq INTEGER PRIMARY KEY AUTOINCREMENT,
 kind TEXT NOT NULL,
 payload TEXT NOT NULL,
 created REAL NOT NULL
);
"""

def _canon(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)

class ResearchLoop:
    """Checkpointed immediate-chaining harness. Caller supplies executor(payload)->result."""
    def __init__(self,db_path):
        self.db=sqlite3.connect(str(db_path)); self.db.executescript(SCHEMA); self.db.commit()

    def enqueue(self,job_id,payload,priority=0.0,parent_id=None):
        now=time.time()
        self.db.execute("INSERT INTO jobs(id,payload,status,priority,parent_id,created,updated) VALUES(?,?,?,?,?,?,?)",
                        (job_id,_canon(payload),"QUEUED",float(priority),parent_id,now,now)); self.db.commit()

    def next_job(self):
        row=self.db.execute("SELECT id,payload FROM jobs WHERE status='QUEUED' ORDER BY priority DESC, created ASC LIMIT 1").fetchone()
        return None if row is None else (row[0],json.loads(row[1]))

    def _event(self,kind,payload):
        self.db.execute("INSERT INTO events(kind,payload,created) VALUES(?,?,?)",(kind,_canon(payload),time.time()))

    def execute_one(self,executor):
        nxt=self.next_job()
        if nxt is None:return None
        job_id,payload=nxt; now=time.time()
        self.db.execute("UPDATE jobs SET status='RUNNING',attempts=attempts+1,updated=? WHERE id=?",(now,job_id)); self._event("JOB_STARTED",{"job_id":job_id}); self.db.commit()
        try:
            result=executor(payload); raw=_canon(result); h=hashlib.sha256(raw.encode()).hexdigest(); now=time.time()
            self.db.execute("INSERT OR REPLACE INTO results(job_id,result,result_sha256,created) VALUES(?,?,?,?)",(job_id,raw,h,now))
            self.db.execute("UPDATE jobs SET status='DONE',updated=? WHERE id=?",(now,job_id)); self._event("JOB_DONE",{"job_id":job_id,"sha256":h}); self.db.commit()
            return {"job_id":job_id,"status":"DONE","result":result,"sha256":h}
        except Exception as e:
            now=time.time(); self.db.execute("UPDATE jobs SET status='FAILED',updated=? WHERE id=?",(now,job_id)); self._event("JOB_FAILED",{"job_id":job_id,"error":type(e).__name__+":"+str(e)}); self.db.commit()
            return {"job_id":job_id,"status":"FAILED","error":str(e)}

    def run_until_empty(self,executor,max_jobs=None,deadline_epoch=None):
        out=[]
        while True:
            if max_jobs is not None and len(out)>=max_jobs:break
            if deadline_epoch is not None and time.time()>=deadline_epoch:break
            if self.next_job() is None:break
            out.append(self.execute_one(executor))
        return out

    def recover_running(self):
        now=time.time(); rows=self.db.execute("SELECT id FROM jobs WHERE status='RUNNING'").fetchall()
        for (job_id,) in rows:
            self.db.execute("UPDATE jobs SET status='QUEUED',updated=? WHERE id=?",(now,job_id)); self._event("JOB_RECOVERED",{"job_id":job_id})
        self.db.commit(); return [r[0] for r in rows]

    def snapshot(self):
        jobs=self.db.execute("SELECT id,status,priority,parent_id,attempts FROM jobs ORDER BY created").fetchall()
        return {"jobs":[{"id":a,"status":b,"priority":c,"parent_id":d,"attempts":e} for a,b,c,d,e in jobs]}
