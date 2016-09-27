e = db.getSiblingDB('epistemonikos');

get_doi = function(id){
  doc = e.documents.findOne({'id' : id})
  return (((doc || {}).info || {}).ids || {}).doi
}

documents = e.documents.find({$and: [{'info.classification' : 'systematic-review'}, {'references.link' : {$exists : true, $nin : ['', null]}}]})
documents.forEach(function(doc){
  (doc.references || []).forEach(function(ref){
      if(ref.link){
        e.references_systematic_review.insert({
          'doi_has_reference' : (doc.info.ids || {}).doi,
          'text_plain' : ref.text_plain,
          'doi_referenced' : get_doi(ref.link)
        })
      }
  })
})
