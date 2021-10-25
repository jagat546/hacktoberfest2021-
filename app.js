const mongoose = require('mongoose');

mongoose.connect("mongodb://localhost:27017/fruitsDB", {userNewUrlParser: true});

const fruitSchema = new mongoose.Schema ({
  name: {
    type: String,
    required: true
  },                                                          //after starting mongo shell, first write show dbs, then use db name then use find
  rating: {
    type: Number,
    min: 1,       // Validators
    max: 10// Validators
  },
  review: String
});

const Fruit = mongoose.model("Fruit", fruitSchema);

const fruit = new Fruit({  //javascript object
//  name: "Apple",
  rating: 10,
  review: "Peaches are so yummy."
});

fruit.save();

const personSchema = new mongoose.Schema ({
  name: String,
  age: Number,
  favoriteFruit: fruitSchema   // we have to update the schema accordingly to use the embedded object in new object
});

const Person = mongoose.model("Person", personSchema);

const pineapple = new Fruit({
  name: "Pineapple",
  score: 9,
  review: "Great fruit"
});

pineapple.save();

const person = new Person({
  name: "Amy",
  age: 12,
  favoriteFruit: pineapple //embedded
});

person.save();

//Person.deleteMany({name: "John"}, function(err){
//  if(err) {
//    console.log(err);
//  } else{
//    console.log("Deleted");
//  }
//});

const kiwi = new Fruit({
  name: "Kiwi",
  score: 10,
  review: "The best fruit!"
});

const orange = new Fruit({
  name: "Orange",
  score: 4,
  review: "Too sour for me"
});

const banana = new Fruit({
  name: "Banana",
  score: 3,
  review: "Wierd texture"
})
Fruit.insertMany([kiwi, orange, banana], function(err){
  if(err){
    console.log(err);
  } else{
    console.log("Successfully saved all fruits to fruitsDB!");
  }
});


Fruit.find(function(err, fruits){
  if(err){
    console.log(err);
  } else{
    mongoose.connection.close();  //so that we do not have to press ctrl+c again and again

  fruits.forEach(function(fruit){
    console.log(fruit.name);
  });
}
});
// Mongoose update and delete and always give a call back function if any error is there
Fruit.updateOne({_id: "616dbb2631fdb72c60db9ff6"}, {name: "Peach"}, function(err){
  if(err){
    console.log(err);
  } else{
    console.log("Successfully updated");
  }

});

Fruit.deleteOne({_id: "616dbb2631fdb72c60db9ff6"}, function(err){
  if(err){
    console.log(err);
  } else{
    console.log("Successfully deleted from the document");
  }
});

const findDocuments = function(db, callback) {
  //Get the documents collection
  const collection = db.collection('fruits');
  //Find some documents
  collection.find({}).toArray(function(err, fruits) {
    assert.equal(err, null);
    console.log("Found the following documents");
    console.log(fruits);
    callback(fruits);
  });
};
