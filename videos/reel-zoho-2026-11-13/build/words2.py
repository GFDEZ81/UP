import json
toks=json.load(open('words.json'))
spans=[(0,2,0.40,1.13),(3,10,1.41,3.63),(11,11,4.26,4.74),(12,14,4.87,6.05),(15,15,6.59,7.09),(16,18,7.31,8.79),(19,22,8.96,9.88),
(23,32,10.25,13.35),(33,41,13.84,15.98),(42,47,16.81,18.37),(48,50,18.78,19.30),(51,55,19.92,21.15),(56,63,21.60,23.48),(64,65,24.02,25.09),(66,70,25.41,26.50)]
out=[]
for a,b,s,e in spans:
    seg=toks[a:b+1]; w=[len(x['text'])+1 for x in seg]; tot=sum(w); c=s
    for x,wi in zip(seg,w):
        d=(e-s)*wi/tot; out.append({"id":f"w{len(out)}","text":x['text'],"start":round(c,3),"end":round(c+d,3)}); c+=d
assert len(out)==71
for o in out: print(o['id'],o['text'],o['start'])
json.dump(out,open('words2.json','w'),ensure_ascii=False)
