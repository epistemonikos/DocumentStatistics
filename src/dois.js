mante = db.getSiblingDB('epistemonikos');
mante.miner_dois.find()
mante.dois.find().forEach(function(s, i){
  if(i % 10000 == 0){
    print(i)
  }
  mante_migration.getCollection(c).insert(s)
})
