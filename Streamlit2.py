<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>Судові справи — Дашборд</title>
<script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
<script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
<style>
body{font-family:sans-serif;margin:20px;}
#filters select,#filters input{margin:5px;}
</style>
</head>
<body>
<h2>Інтерактивний дашборд судових справ</h2>
<p>Завантаж CSV (raw GitHub або локально) — поля: <b>region, article, date, category</b></p>
<input type="file" id="file"><br>
<input type="text" id="url" placeholder="https://raw.githubusercontent.com/.../data.csv" size="60">
<button onclick="loadUrl()">Завантажити з URL</button>

<div id="filters">
  <select id="region"></select>
  <select id="article"></select>
  Від <input type="date" id="from"> До <input type="date" id="to">
  <button onclick="update()">Фільтрувати</button>
</div>

<div id="chart"></div>
<div id="trend"></div>

<script>
let data=[]
document.getElementById("file").addEventListener("change",e=>{
  Papa.parse(e.target.files[0],{header:!0,complete:r=>init(r.data)})
})
function loadUrl(){
  Papa.parse(document.getElementById("url").value,{download:!0,header:!0,complete:r=>init(r.data)})
}
function init(d){
  data=d.map(r=>({region:r.region,article:r.article,date:new Date(r.date),category:r.category}))
  fill("region",[...new Set(data.map(r=>r.region))])
  fill("article",[...new Set(data.map(r=>r.article))])
  update()
}
function fill(id,vals){
  let s=document.getElementById(id);s.innerHTML='<option value=\"\">(всі)</option>'+vals.map(v=><option>${v}</option>).join('')
}
function filter(){
  let r=document.getElementById("region").value,a=document.getElementById("article").value
  let f=document.getElementById("from").value?new Date(document.getElementById("from").value):null
  let t=document.getElementById("to").value?new Date(document.getElementById("to").value):null
  return data.filter(x=>(!r||x.region==r)&&(!a||x.article==a)&&(!f||x.date>=f)&&(!t||x.date<=t))
}
function update(){
  let d=filter()
  let catCount={}
  d.forEach(x=>catCount[x.category]=(catCount[x.category]||0)+1)
  Plotly.newPlot('chart',[{type:'bar',x:Object.keys(catCount),y:Object.values(catCount)}],
    {title:'Кількість справ за категоріями'})
  let yearCount={}
  d.forEach(x=>{let y=x.date.getFullYear();yearCount[y]=(yearCount[y]||0)+1})
  Plotly.newPlot('trend',[{type:'scatter',x:Object.keys(yearCount),y:Object.values(yearCount)}],
    {title:'Тренд по роках'})
}
</script>
</body>
</html>
