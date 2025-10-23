from app import app, db, Person

# Training data from the image
X = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37],
     [166, 65, 40], [190, 90, 47], [175, 64, 39], [177, 70, 40], [159, 55, 37],
     [171, 75, 42], [181, 85, 43]]

Y = ['male', 'female', 'female', 'female',
     'male', 'male', 'male', 'female', 'male',
     'female', 'male']


def delete_entries():
    with app.app_context():
        persons_to_delete = Person.query.filter(Person.id > 11).all()

        if persons_to_delete:
            for person in persons_to_delete:
                db.session.delete(person)
            db.session.commit()
            print(f"Deleted {len(persons_to_delete)} entries with ID > 11")
        else:
            print("No entries with ID > 11 found")


def populate_database():
    with app.app_context():
        # Clear existing data
        Person.query.delete()

        # Add all training data
        for i in range(len(X)):
            height, weight, shoe_size = X[i]
            gender = Y[i]

            person = Person(
                height=height,
                weight=weight,
                shoe_size=shoe_size,
                gender=gender
            )
            db.session.add(person)

        # Commit all changes
        db.session.commit()
        print(f"Successfully added {len(X)} records to the database!")

        # Verify the data
        all_persons = Person.query.all()
        print(f"\nTotal records in database: {len(all_persons)}")
        for person in all_persons:
            print(f"ID: {person.id}, Height: {person.height}, Weight: {person.weight}, "
                  f"Shoe Size: {person.shoe_size}, Gender: {person.gender}")


if __name__ == '__main__':
    populate_database()
    # delete_entries()
