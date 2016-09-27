e = db.getSiblingDB('epistemonikos');
e.documents.createIndex({
  'id' : 1
},{
  background: true
})
