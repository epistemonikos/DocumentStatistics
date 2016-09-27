e = db.getSiblingDB('epistemonikos');
e.references_systematic_review.find({'doi_referenced' : {$ne : null}}).forEach(function(doc){
  print(doc.doi_referenced+'\t'+doc.text_plain)
})
