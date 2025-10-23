from app import app, db, Person

def view_database():
    with app.app_context():
        # Get all persons from database
        all_persons = Person.query.all()
        
        print(f"\n{'='*70}")
        print(f"Total records in database: {len(all_persons)}")
        print(f"{'='*70}\n")
        
        if not all_persons:
            print("Database is empty!")
        else:
            # Print header
            print(f"{'ID':<5} {'Height (cm)':<12} {'Weight (kg)':<12} {'Shoe Size':<12} {'Gender':<10}")
            print(f"{'-'*70}")
            
            # Print each person
            for person in all_persons:
                print(f"{person.id:<5} {person.height:<12} {person.weight:<12} "
                      f"{person.shoe_size:<12} {person.gender:<10}")
            
            print(f"{'-'*70}\n")
            
            # Print summary statistics
            males = [p for p in all_persons if p.gender == 'male']
            females = [p for p in all_persons if p.gender == 'female']
            
            print(f"Summary:")
            print(f"  Males: {len(males)}")
            print(f"  Females: {len(females)}")
            print(f"{'='*70}\n")

if __name__ == '__main__':
    view_database()