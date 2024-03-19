# Run: python .\manage.py breed_group_data
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from store.models import Group, Breed


class Command(BaseCommand):
    help = "Populates Group and Breed models with initial data"

    def handle(self, *args, **options):
        data = {
            "Herding Group": "These intelligent and hardworking dogs were developed to assist in herding livestock, showcasing remarkable obedience and agility. Breeds like the Border Collie and Australian Shepherd are renowned for their ability to anticipate and control the movement of animals. With their strong work ethic and quick learning, they thrive in activities like herding trials and obedience competitions. Their natural instinct to herd extends to their human families, making them loyal and protective companions.",
            "Non-Sporting Group": "This diverse group encompasses breeds with varied appearances and temperaments, reflecting their historical roles as companions rather than specialized workers. From the sturdy Bulldog to the elegant Poodle, each breed brings unique qualities to the table. While some, like the Dalmatian, may have originally served as carriage dogs, others like the Boston Terrier were bred solely for companionship. Non-sporting dogs are characterized by their adaptability and suitability for a wide range of lifestyles.",
            "Toy Group": "Toy dogs are cherished for their diminutive size, making them ideal companions for those living in smaller spaces. Despite their tiny stature, breeds like the Chihuahua and Pomeranian are brimming with personality and confidence. They thrive on human companionship and enjoy being pampered as indoor pets. Despite their small size, they often possess a bold and spirited demeanor, making them delightful companions for individuals or families looking for a compact yet charismatic pet.",
            "Terrier Group": "Known for their feisty personalities and boundless energy, terriers were originally bred for hunting vermin and small game. From the agile Jack Russell Terrier to the muscular Bull Terrier, these dogs possess a relentless determination and tenacity. Terriers require plenty of mental and physical stimulation to channel their energy positively. Their intelligence and strong prey drive make them adept at activities like earthdog trials and agility competitions. While they can be independent-minded, they form strong bonds with their families and are fiercely loyal.",
            "Working Group": "Bred for tasks requiring strength, endurance, and intelligence, working dogs excel in various roles such as guarding, pulling sleds, and performing search and rescue missions. Breeds like the German Shepherd and Siberian Husky are highly trainable and possess a strong sense of duty to their human companions. Whether serving as police K-9s or assisting with therapy work, working dogs demonstrate remarkable versatility and dedication. They require regular exercise and mental stimulation to thrive, as well as a sense of purpose in their daily activities.",
            "Hound Group": "Hounds are characterized by their exceptional scenting ability and endurance, making them proficient hunters and trackers. From the swift Greyhound to the persistent Bloodhound, breeds in this group excel in activities like scent work, tracking, and lure coursing. Hounds are known for their independent nature and can be single-minded when on the trail of a scent. While they may be less biddable than some other breeds, they form strong bonds with their families and thrive on companionship. Hound owners should provide ample opportunities for exercise and mental stimulation to satisfy their innate hunting instincts.",
            "Sporting Group": "Sporting dogs are prized for their athleticism, intelligence, and versatility in various outdoor activities. From the water-loving Labrador Retriever to the agile Spaniel breeds, these dogs excel in hunting, retrieving, and competitive sports like agility and flyball. Sporting dogs thrive on regular exercise and mental stimulation and form strong bonds with their human companions. They are known for their friendly and sociable nature, making them excellent family pets. Whether in the field or in the home, sporting dogs are happiest when given the opportunity to engage in activities that cater to their natural instincts.",
        }

        breed_data = {
            "Herding Group": [
                "Australian Cattle Dog",
                "Australian Shepherd",
                "Bearded Collie",
                "Belgian Malinois",
                "Belgian Sheepdog",
                "Belgian Tervuren",
                "Bergamasco",
                "Berger Picard",
                "Border Collie",
                "Bouvier des Flandres",
                "Briard",
                "Canaan Dog",
                "Cardigan Welsh Corgi",
                "Collie",
                "Entlebucher Mountain Dog",
                "Finnish Lapphund",
                "German Shepherd Dog",
                "Icelandic Sheepdog",
                "Miniature American Shepherd",
                "Norwegian Buhund",
                "Old English Sheepdog",
                "Pembroke Welsh Corgi",
                "Polish Lowland Sheepdog",
                "Puli",
                "Pumi",
                "Pyrenean Shepherd",
                "Shetland Sheepdog",
                "Spanish Water Dog",
                "Swedish Vallhund",
            ],
            "Non-Sporting Group": [
                "American Eskimo Dog",
                "Bichon Frise",
                "Boston Terrier",
                "Bulldog",
                "Chinese Shar-Pei",
                "Chow Chow",
                "Dalmatian",
                "French Bulldog",
                "Keeshond",
                "Lhasa Apso",
                "Lowchen",
                "Poodle",
                "Schipperke",
                "Shiba Inu",
                "Tibetan Spaniel",
                "Tibetan Terrier",
            ],
            "Toy Group": [
                "Affenpinscher",
                "Brussels Griffon",
                "Cavalier King Charles Spaniel",
                "Chihuahua",
                "Chinese Crested",
                "English Toy Spaniel",
                "Havanese",
                "Italian Greyhound",
                "Japanese Chin",
                "Maltese",
                "Manchester Terrier (Toy)",
                "Miniature Pinscher",
                "Papillon",
                "Pekingese",
                "Pomeranian",
                "Poodle (Toy)",
                "Pug",
                "Shih Tzu",
                "Silky Terrier",
                "Toy Fox Terrier",
                "Yorkshire Terrier",
            ],
            "Terrier Group": [
                "Airedale Terrier",
                "American Hairless Terrier",
                "American Staffordshire Terrier",
                "Australian Terrier",
                "Bedlington Terrier",
                "Border Terrier",
                "Bull Terrier",
                "Cairn Terrier",
                "Cesky Terrier",
                "Dandie Dinmont Terrier",
                "Glen of Imaal Terrier",
                "Irish Terrier",
                "Kerry Blue Terrier",
                "Lakeland Terrier",
                "Manchester Terrier",
                "Miniature Bull Terrier",
                "Miniature Schnauzer",
                "Norfolk Terrier",
                "Norwich Terrier",
                "Parson Russell Terrier",
                "Rat Terrier",
                "Russell Terrier",
                "Scottish Terrier",
                "Sealyham Terrier",
                "Skye Terrier",
                "Smooth Fox Terrier",
                "Soft Coated Wheaten Terrier",
                "Staffordshire Bull Terrier",
                "Welsh Terrier",
                "West Highland White Terrier",
                "Wire Fox Terrier",
            ],
            "Working Group": [
                "Akita",
                "Alaskan Malamute",
                "Anatolian Shepherd Dog",
                "Bernese Mountain Dog",
                "Boerboel",
                "Boxer",
                "Bullmastiff",
                "Cane Corso",
                "Doberman Pinscher",
                "Dogue de Bordeaux",
                "German Pinscher",
                "Giant Schnauzer",
                "Great Dane",
                "Great Pyrenees",
                "Greater Swiss Mountain Dog",
                "Komondor",
                "Kuvasz",
                "Leonberger",
                "Mastiff",
                "Neapolitan Mastiff",
                "Newfoundland",
                "Portuguese Water Dog",
                "Rottweiler",
                "Saint Bernard",
                "Samoyed",
                "Siberian Husky",
                "Standard Schnauzer",
                "Tibetan Mastiff",
            ],
            "Hound Group": [
                "Afghan Hound",
                "American English Coonhound",
                "American Foxhound",
                "Basenji",
                "Basset Hound",
                "Beagle",
                "Black and Tan Coonhound",
                "Bloodhound",
                "Bluetick Coonhound",
                "Borzoi",
                "Cirneco dell'Etna",
                "Dachshund",
                "English Foxhound",
                "Greyhound",
                "Harrier",
                "Ibizan Hound",
                "Irish Wolfhound",
                "Norwegian Elkhound",
                "Otterhound",
                "Petit Basset Griffon Vendéen",
                "Pharaoh Hound",
                "Plott",
                "Portuguese Podengo",
                "Redbone Coonhound",
                "Rhodesian Ridgeback",
                "Saluki",
                "Scottish Deerhound",
                "Sloughi",
                "Treeing Walker Coonhound",
                "Whippet",
            ],
            "Sporting Group": [
                "American Cocker Spaniel",
                "American Water Spaniel",
                "Barbet",
                "Boykin Spaniel",
                "Brittany",
                "Chesapeake Bay Retriever",
                "Clumber Spaniel",
                "Curly-Coated Retriever",
                "English Cocker Spaniel",
                "English Setter",
                "English Springer Spaniel",
                "Field Spaniel",
                "Flat-Coated Retriever",
                "German Shorthaired Pointer",
                "German Wirehaired Pointer",
                "Golden Retriever",
                "Gordon Setter",
                "Irish Red and White Setter",
                "Irish Setter",
                "Irish Water Spaniel",
                "Lagotto Romagnolo",
                "Labrador Retriever",
                "Nova Scotia Duck Tolling Retriever",
                "Pointer",
                "Spinone Italiano",
                "Sussex Spaniel",
                "Vizsla",
                "Weimaraner",
                "Welsh Springer Spaniel",
                "Wirehaired Pointing Griffon",
            ],
        }

        for group_name, description in data.items():
            try:
                group = Group.objects.create(name=group_name, description=description)
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created Group: {group_name}")
                )
            except:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to create Group (already exists): {group_name}. Skipping..."
                    )
                )

        for group_name, breeds in breed_data.items():
            group = Group.objects.get(name=group_name)
            for breed_name in breeds:
                try:
                    breed = Breed.objects.create(name=breed_name, group=group)
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully created Breed: {breed_name}")
                    )
                except IntegrityError:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed to create Breed (already exists): {breed_name}. Skipping..."
                        )
                    )
