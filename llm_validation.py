from typing import Dict, List, Set
import re

class PetValidationError(Exception):
    """Custom exception for pet data validation errors"""
    pass

class PetDataValidator:
    def __init__(self):
        # Common dog breeds
        self.dog_breeds: Set[str] = {
            "Affenpinscher", "American Bulldog", "English Setter", "English Shepherd", "English Springer Spaniel", "English Toy Spaniel", "English Toy Terrier", "Eurasier", "Field Spaniel", 
            "American Bully", "Finnish Lapphund", "Finnish Spitz", "French Bulldog", "German Pinscher", "German Shepherd Dog", "German Shorthaired Pointer", "Giant Schnauzer", "American Eskimo Dog", 
            "Glen of Imaal Terrier", "Golden Retriever", "Gordon Setter", "Great Dane", "Great Pyrenees", "Greyhound", "Griffon Bruxellois", "Harrier", "American Eskimo Dog (Miniature)", "Havanese", 
            "Irish Setter", "Irish Terrier", "Irish Wolfhound", "Italian Greyhound", "American Foxhound", "Japanese Chin", "Japanese Spitz", "Keeshond", "Komondor", "Kooikerhondje", "Kuvasz", 
            "Labrador Retriever", "American Pit Bull Terrier", "Lagotto Romagnolo", "Lancashire Heeler", "Leonberger", "Poodle (Toy)", "Lhasa Apso", "American Staffordshire Terrier", "Maltese", 
            "Miniature American Shepherd", "Miniature Pinscher", "Miniature Schnauzer", "American Water Spaniel", "Newfoundland", "Norfolk Terrier", "Norwich Terrier", "Nova Scotia Duck Tolling Retriever", 
            "Old English Sheepdog", "Olde English Bulldogge", "Anatolian Shepherd Dog", "Papillon", "Pekingese", "Pembroke Welsh Corgi", "Perro de Presa Canario", "Pharaoh Hound", "Plott", "Appenzeller Sennenhund", 
            "Pomeranian", "Poodle (Miniature)", "Afghan Hound", "Australian Cattle Dog", "Pug", "Puli", "Pumi", "Rat Terrier", "Redbone Coonhound", "Rhodesian Ridgeback", "Australian Kelpie", "Rottweiler", 
            "Russian Toy", "Saint Bernard", "Saluki", "Samoyed", "Schipperke", "Scottish Deerhound", "Scottish Terrier", "Australian Shepherd", "Shetland Sheepdog", "Shiba Inu", "Shih Tzu", "Shiloh Shepherd", 
            "Siberian Husky", "Silky Terrier", "Australian Terrier", "Smooth Fox Terrier", "Soft Coated Wheaten Terrier", "Spanish Water Dog", "Spinone Italiano", "Staffordshire Bull Terrier", "Standard Schnauzer", 
            "Azawakh", "Swedish Vallhund", "Thai Ridgeback", "Tibetan Mastiff", "Tibetan Spaniel", "Tibetan Terrier", "Toy Fox Terrier", "Barbet", "Treeing Walker Coonhound", "Vizsla", "Weimaraner", "Welsh Springer Spaniel", 
            "Whippet", "West Highland White Terrier", "Akbash Dog", "White Shepherd", "Wire Fox Terrier", "Basenji", "Wirehaired Pointing Griffon", "Wirehaired Vizsla", "Xoloitzcuintli", "Yorkshire Terrier", 
            "Basset Bleu de Gascogne", "African Hunting Dog", "Basset Hound", "Beagle", "Bearded Collie", "Beauceron", "Bedlington Terrier", "Belgian Malinois", "Belgian Tervuren", "Airedale Terrier", 
            "Bernese Mountain Dog", "Bichon Frise", "Black and Tan Coonhound", "Bloodhound", "Bluetick Coonhound", "Boerboel", "Border Collie", "Border Terrier", "Boston Terrier", "Bouvier des Flandres", "Boxer", 
            "Boykin Spaniel", "Bracco Italiano", "Briard", "Brittany", "Akita", "Bull Terrier", "Bullmastiff", "Cairn Terrier", "Cane Corso", "Cardigan Welsh Corgi", "Catahoula Leopard Dog", "Alapaha Blue Blood Bulldog", 
            "Caucasian Shepherd (Ovcharka)", "Cavalier King Charles Spaniel", "Chesapeake Bay Retriever", "Chinese Crested", "Chinese Shar-Pei", "Alaskan Husky", "Chinook", "Chow Chow", "Clumber Spaniel", "Cocker Spaniel", 
            "Cocker Spaniel (American)", "Coton de Tulear", "Alaskan Malamute", "Dalmatian", "Doberman Pinscher", "Dogo Argentino", "Dutch Shepherd", "Mix Breed"
        }
        
        # Common cat breeds
        self.cat_breeds: Set[str] = {
            "American Bobtail", "Abyssinian", "American Curl", "Aegean", "Arabian Mau", "Australian Mist", "American Shorthair", "American Wirehair", "Balinese", "Bambino", "Bengal", 
            "Birman", "Bombay", "British Shorthair", "British Longhair", "Burmese", "Burmilla", "Chartreux", "Chausie", "Cheetoh", "Cornish Rex", "Colorpoint Shorthair", "California Spangled", 
            "Chantilly-Tiffany", "Cymric", "Cyprus", "Donskoy", "Devon Rex", "Siberian", "European Burmese", "Egyptian Mau", "Exotic Shorthair", "Havana Brown", "Himalayan", "Javanese", 
            "Japanese Bobtail", "Khao Manee", "Korat", "Kurilian", "LaPerm", "Dragon Li", "Malayan", "Manx", "Maine Coon", "Mix Breed", "Munchkin", "Nebelung", "Norwegian Forest Cat", 
            "Ocicat", "Oriental", "Persian", "Pixie-bob", "Ragamuffin", "Ragdoll", "Russian Blue", "Savannah", "Scottish Fold", "Siamese", "Singapura", "Snowshoe", "Somali", "Sphynx", 
            "Selkirk Rex", "Turkish Angora", "Tonkinese", "Toyger", "Turkish Van", "York Chocolate"
        }

    def validate_breed(self, breed: str, species: str) -> bool:
        # Normalize the input breed and species
        normalized_breed: str = breed.strip().title()  # Capitalize first letter of each word
        normalized_species: str = species.lower().strip()
        
        # Create normalized breed sets
        normalized_dog_breeds: Set[str] = {breed.title() for breed in self.dog_breeds}
        normalized_cat_breeds: Set[str] = {breed.title() for breed in self.cat_breeds}
        
        if normalized_species == "dog":
            return normalized_breed in normalized_dog_breeds
        elif normalized_species == "cat":
            return normalized_breed in normalized_cat_breeds
        return False

    def validate_numeric(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_pet_data(self, pet_data: Dict) -> Dict:
        errors = []
        
        # Validate breed
        if not self.validate_breed(pet_data.get('breed', ''), pet_data.get('species', '')):
            errors.append(f"Invalid breed '{pet_data.get('breed', '')}' for {pet_data.get('species', '')}")
        
        # Validate age
        if not self.validate_numeric(str(pet_data.get('age', ''))):
            errors.append("Age must be a number")
            
        # Validate weight
        if not self.validate_numeric(str(pet_data.get('weight', ''))):
            errors.append("Weight must be a number")
        
        if errors:
            raise PetValidationError("\n".join(errors))
            
        
        return pet_data