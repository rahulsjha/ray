import time, requests, subprocess, ray
from ray import serve
D="http://localhost:8265"
def replicas():
    d=requests.get(f"{D}/api/serve/applications/").json()
    out={}
    for an,a in d["applications"].items():
        for dn,dep in a["deployments"].items():
            out[(an,dn)]=sorted(r["replica_id"] for r in dep["replicas"] if r["state"]=="RUNNING")
    return out
def wait(cond,t=120):
    for _ in range(t):
        if cond(): return True
        time.sleep(1)
    return False
subprocess.run(["serve","deploy","config.yaml"],check=True)
ray.init(address="auto"); serve.run(__import__("toy").other, name="imperative_app", route_prefix="/other")
assert wait(lambda: len(replicas().get(("default","Translator"),[]))==1 and len(replicas().get(("default","Summarizer"),[]))==1)
before=replicas(); print("before:", {k:len(v) for k,v in before.items()})
exec(open("doc_example.py").read())
assert wait(lambda: len(replicas().get(("default","Translator"),[]))==3), "Translator did not scale to 3"
after=replicas(); print("after: ", {k:len(v) for k,v in after.items()})
assert set(before[("default","Translator")]) <= set(after[("default","Translator")]), "Translator replica restarted"
assert before[("default","Summarizer")]==after[("default","Summarizer")], "Summarizer restarted"
assert before[("imperative_app","Other")]==after[("imperative_app","Other")], "serve.run app touched"
print("OK: Translator scaled 1->3 keeping its replica; Summarizer and the serve.run app untouched")
