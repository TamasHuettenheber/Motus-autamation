#!/usr/bin/env python3
"""Schedule validated Jori episodes 002–010; never touch MOTUS."""
import argparse,json,os,time,urllib.request,urllib.error
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
p=argparse.ArgumentParser();p.add_argument("--episode",type=int,required=True,choices=[2,3,4,5,6,7,8,9,10]);p.add_argument("--replace-existing",action="store_true");a=p.parse_args()
n=a.episode
key=os.environ.get("BUFFER_API_KEY","").strip()
assert key,"BUFFER_API_KEY_MISSING"
due=datetime(2026,10,22+n-1,14,0,tzinfo=ZoneInfo("Europe/Berlin"))
assert datetime.now(ZoneInfo("Europe/Berlin"))<due,"Requested publishing time passed"
expected_due_utc=due.astimezone(timezone.utc)
if n in (6,7,8,9,10):
    release_path=f"kids/jori-flimm/relaunch-v2/episode_{n:03d}_release_record.json"
    release=json.loads(open(release_path,encoding="utf-8").read())
    assert release.get("user_approved_for_publication") is True,f"Episode {n:03d} has no explicit user release approval"
    assert datetime.fromisoformat(release.get("target_due_at","")).astimezone(timezone.utc)==expected_due_utc,f"Episode {n:03d} release target differs from the fixed 14:00 slot"
    if n==6:
        assert release.get("speech_caption_offset_accepted") is True,"Episode 006's accepted ending offset is not recorded"
    if n==7:
        assert release.get("render_qc_passed") is True and release.get("video_path")=="published/jori-flimm-2026-10-28-e007-v1.mp4","Episode 007 has no passing render QC record"
    if n==8:
        assert release.get("render_qc_passed") is True and release.get("video_path")=="published/jori-flimm-2026-10-29-e008-v2.mp4","Episode 008 has no passing render QC record"
    if n==9:
        assert release.get("render_qc_passed") is True and release.get("video_path")=="published/jori-flimm-2026-10-30-e009-v2.mp4","Episode 009 has no passing render QC record"
    if n==10:
        assert release.get("render_qc_passed") is True and release.get("video_path")=="published/jori-flimm-2026-10-31-e010-v2.mp4","Episode 010 has no passing render QC record"
        assert release.get("final_qc_run_id") and release.get("queue_check_run_id"),"Episode 010 is missing final QC or live queue verification"
repo=os.environ["GITHUB_REPOSITORY"]
version_suffix={6:"-v2",7:"-v1",8:"-v2",9:"-v2",10:"-v2"}.get(n,"")
media=f"https://raw.githubusercontent.com/{repo}/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-{22+n-1:02d}-e{n:03d}{version_suffix}.mp4"
def gql(query,variables=None):
 req=urllib.request.Request("https://api.buffer.com",method="POST",data=json.dumps({"query":query,"variables":variables or {}}).encode(),headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
 try:
  with urllib.request.urlopen(req,timeout=45) as resp:result=json.load(resp)
 except urllib.error.HTTPError as exc:raise RuntimeError(f"Buffer HTTP {exc.code}: {exc.read()[:400]!r}")
 if result.get("errors"):raise RuntimeError(str(result["errors"]))
 return result["data"]
for attempt in range(16):
 try:
  with urllib.request.urlopen(urllib.request.Request(media,method="HEAD"),timeout=20) as resp:
   if resp.status==200 and int(resp.headers.get("Content-Length","0"))>1000000:break
 except Exception:pass
 time.sleep(5)
else:raise RuntimeError("Public GitHub MP4 not reachable; refusing Buffer")
orgs=gql("query{account{organizations{id name}}}")["account"]["organizations"]
matches=[]
for org in orgs:
 channels=gql("query($id:OrganizationId!){channels(input:{organizationId:$id}){id name displayName service}}",{"id":org["id"]})["channels"]
 for c in channels:
  names={str(c.get(k,"")).strip().lower().lstrip("@") for k in ["name","displayName"]}
  if str(c.get("service","")).lower()=="tiktok" and "jori.flimm" in names:matches.append((org["id"],c["id"]))
assert len(matches)==1,"Jori channel not uniquely verified; MOTUS must not be used"
oid,channel=matches[0]
query="query{posts(input:{organizationId:"+json.dumps(oid)+",filter:{status:[scheduled],channelIds:["+json.dumps(channel)+"]}}){edges{node{id text dueAt channelId}}pageInfo{hasNextPage}}}"
posts=gql(query)["posts"]
assert not posts["pageInfo"]["hasNextPage"],"Cannot check all scheduled posts"
scheduled_nodes=[edge["node"] for edge in posts["edges"]]
slot_conflicts=[x for x in scheduled_nodes
                if datetime.fromisoformat(x["dueAt"].replace("Z","+00:00")).astimezone(timezone.utc)==expected_due_utc
                and f"Jori & Flimm | Folge {n:03d}" not in (x.get("text") or "")]
assert not slot_conflicts,{"target_slot_already_occupied":slot_conflicts}
existing=[]
for edge in posts["edges"]:
 old=edge["node"]
 if f"Jori & Flimm | Folge {n:03d}" in (old.get("text") or ""):
  existing.append(old)
if a.replace_existing:
 assert len(existing)==1,"Scheduled episode post is not unique; refusing replacement"
 old=existing[0]
 mutation="""mutation($input:EditPostInput!){editPost(input:$input){__typename ... on PostActionSuccess{post{id status dueAt channelId assets{mimeType source}}} ... on MutationError{message}}}"""
 edited=gql(mutation,{"input":{"id":old["id"],"assets":[{"video":{"url":media,"metadata":{"thumbnailOffset":1000}}}]}})["editPost"]
 assert edited.get("__typename")=="PostActionSuccess",edited
 post=edited["post"]
 assert post.get("id")==old["id"] and post.get("status")=="scheduled" and post.get("channelId")==channel,post
 assert post.get("dueAt")==old.get("dueAt"),{"before":old.get("dueAt"),"after":post.get("dueAt")}
 assert any(x.get("source")==media for x in post.get("assets",[])),post
 print("JORI_BUFFER_POST_UPDATED_IN_PLACE",n,json.dumps(post,ensure_ascii=False))
 raise SystemExit(0)
if existing:
 assert len(existing)==1,"Duplicate scheduled episode posts detected"
 old=existing[0]
 assert datetime.fromisoformat(old["dueAt"].replace("Z","+00:00")).astimezone(timezone.utc)==expected_due_utc,{"actual_dueAt":old.get("dueAt"),"expected_dueAt":due.isoformat()}
 print("JORI_EPISODE_ALREADY_SCHEDULED",n,old["id"],old["dueAt"])
 raise SystemExit(0)
if n in (6,7,8,9,10):
 e=json.loads(open(f"kids/jori-flimm/relaunch-v2/episode_{n:03d}_story_draft.json",encoding="utf-8").read())
else:
 data=json.loads(open("kids/jori-flimm/relaunch-v2/staffel1_folgen_001_005.json",encoding="utf-8").read())
 e=next(x for x in data["episodes"] if x["episode_number"]==n)
caption=f"Jori & Flimm | Folge {n:03d}: {e['title']}. Die Geschichte geht weiter – mit einem neuen Rätsel! #JoriUndFlimm #Kindergeschichte #Rätsel #GeschichtenFürKinder"
mutation="""mutation($input:CreatePostInput!){createPost(input:$input){__typename ... on PostActionSuccess{post{id status dueAt channelId assets{mimeType source}}} ... on MutationError{message}}}"""
result=gql(mutation,{"input":{"text":caption,"channelId":channel,"schedulingType":"automatic","mode":"customScheduled","dueAt":due.isoformat(timespec="milliseconds"),"aiAssisted":True,"metadata":{"tiktok":{"isAiGenerated":True}},"assets":[{"video":{"url":media,"metadata":{"thumbnailOffset":1000}}}]}})["createPost"]
assert result.get("__typename")=="PostActionSuccess",result
post=result["post"]
assert post.get("status")=="scheduled" and post.get("channelId")==channel,post
assert datetime.fromisoformat(post["dueAt"].replace("Z","+00:00")).astimezone(timezone.utc)==expected_due_utc,{"actual_dueAt":post.get("dueAt"),"expected_dueAt":due.isoformat()}
print("JORI_BUFFER_SCHEDULED_CONFIRMED",n,json.dumps(post,ensure_ascii=False))
