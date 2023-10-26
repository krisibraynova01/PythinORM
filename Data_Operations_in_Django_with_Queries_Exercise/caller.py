import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet
from main_app.models import Artifact
from main_app.models import Location
from main_app.models import Car
from main_app.models import Task
from main_app.models import HotelRoom
from main_app.models import Character


# Create queries within functions

# 01. Pet
def create_pet(name, species):
    Pet.objects.create(name=name, species=species)

    return f"{name} is a very cute {species}!"

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# 02. Artifact
def create_artifact(name, origin, age, description, is_magical):
    Artifact.objects.create(name=name,
                            origin=origin,
                            age=age,
                            description=description,
                            is_magical=is_magical)

    return f"The artifact {name} is {age} years old!"

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune', True))

def delete_all_artifacts():
    Artifact.objects.all().delete()

# delete_all_artifacts()
# print(f"{Artifact.objects.count()}")

# 03. Location
def create_location(name,region,population,description,is_capital):
    Location.objects.create(
        name=name,
        region=region,
        population=population,
        description=description,
        is_capital=is_capital
    )

# create_location('Sofia','Sofia Region',1329000,'The capital of Bulgaria and the largest city in the country',False)
# create_location('Plovdiv','Plovdiv Region',346942,'The second-largest city in Bulgaria with a rich historical heritage',False)
# create_location('Varna','Varna Region',330486,'A city known for its sea breeze and beautiful beaches on the Black Sea',False)
# print(Location.objects.all())

def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    locations_info = [f"{location.name} has a population of {location.population}!" for location in locations]
    return "\n".join(locations_info)

# print(show_all_locations())

def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()

def get_capitals():
    capital = Location.objects.filter(is_capital=True).values('name')
    return capital

# print(get_capitals())

def delete_first_location():
    first_location = Location.objects.first()
    first_location.delete()

# delete_first_location()

# 04.Car
def create_car(model, year, color, price):
    Car.objects.create(
        model=model,
        year=year,
        color=color,
        price=price
    )


# create_car('Mercedes C63 AMG', 2019, 'white', 120000)
# create_car('Audi Q7 S line', 2023, 'black', 183900)
# create_car('Chevrolet Corvette', 2021, 'dark grey', 199999)

def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        percentage = 1 - sum(int(x) for x in str(car.year)) / 100
        car.price_with_discount = float(car.price) * percentage
        car.save()

#  apply_discount()

def get_recent_cars():
    filtered_cars = Car.objects.filter(year__gte=2020).values('model','price_with_discount')
    return filtered_cars

# print(get_recent_cars())

def delete_last_car():
    Car.objects.last().delete()

# delete_last_car()

# 05.Task Encoder
def create_task(title, description, due_date, is_finished):
    Task.objects.create(
        title=title,
        description=description,
        due_date=due_date,
        is_finished=is_finished
    )

# create_task('Simple Task', 'This is a sample task description','2023-10-31',False)
# create_task('Simple Task2', 'This is a sample task description','2023-11-01',False)
# create_task('Simple Task3', 'This is a sample task description','2023-11-02',False)

def show_unfinished_tasks():
    not_finished_task = Task.objects.filter(is_finished=False)
    result = []
    for task in not_finished_task:
        result.append(f"Task - {task.title} needs to be done until {task.due_date}!")
    return '\n'.join(result)

# print(show_unfinished_tasks())

def complete_odd_tasks():
    tasks = Task.objects.all()
    for task in tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()

def encode_and_replace(text, task_title):
    tasks = Task.objects.filter(title = task_title)
    encoded_text = ''

    for char in text:
        encoded_text += chr(ord(char) - 3)

    for task in tasks:
        task.description = encoded_text
        task.save()

# # encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")

# 06. Hotel Room
def create_room(room_number, room_type, capacity, amenities, price_per_night):
    new_room = HotelRoom.objects.create(
        room_number=room_number,
        room_type=room_type,
        capacity=capacity,
        amenities=amenities,
        price_per_night=price_per_night
    )


# create_room(101, 'Standard', 2, 'Tv', 100)
# create_room(201, 'Deluxe', 3, 'Wi-Fi', 200)
# create_room(501, 'Deluxe', 6, 'Jacuzzi', 400)

def get_deluxe_rooms():
    rooms = HotelRoom.objects.filter(room_type='Deluxe')
    result = []
    for room in rooms:
        if room.id % 2 == 0:
            result.append(f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!')
    return '\n'.join(result)


print(get_deluxe_rooms())

def increase_room_capacity():
     rooms = HotelRoom.objects.order_by('id')

     for idx, room in enumerate(rooms):
         if room.is_reserved:
             if idx == 0:
                 room.capacity += room.id
             elif room.is_reserved:
                 room.capacity += rooms[idx - 1].capacity
             room.save()

# increase_room_capacity()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


# reserve_first_room()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved:
        last_room.delete()


# delete_last_room()

# 07. Character
def update_characters():
    Character.objects.filter(class_name='Mage').update(level=F('level')+3,
                                                intelligence = F('intelligence') - 7)
    Character.objects.filter(class_name='Warrior').update(hit_points=F('hit_points') / 2,
                                                       dexterity=F('dexterity') + 4)
    Character.objects.filter(class_name__in=('Assassin','Scout')).update(inventory='The inventory is empty')

def fuse_characters(first_character, second_character):
    inventory = ''
    if first_character.class_name in ('Mage', 'Scout'):
        inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    elif first_character.class_name in ('Warrior', 'Assassin'):
        inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=f'{first_character.name} {second_character.name}',
        class_name="Fusion",
        level=int((first_character.level + second_character.level) // 2),
        strength=int((first_character.strength + second_character.strength) * 1.2),
        dexterity=int((first_character.dexterity + second_character.dexterity) * 1.4),
        intelligence=int((first_character.intelligence + second_character.intelligence) * 1.5),
        hit_points=int(first_character.hit_points + second_character.hit_points),
        inventory=inventory,
    )
    first_character.delete()
    second_character.delete()

def grand_dexterity():
    Character.objects.update(dexterity=30)


# grand_dexterity()

def grand_intelligence():
    Character.objects.update(intelligence=40)


# grand_intelligence()

def grand_strength():
    Character.objects.update(strength=50)


# grand_strength()

def delete_characters():
    Character.objects.filter(inventory__contains='The inventory is empty').delete()

# delete_characters()

# character1 = Character.objects.create(
#     name="Gandalf",
#     class_name="Mage",
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory="Staff of Magic, Spellbook",
# )
#
# character2 = Character.objects.create(
#     name="Hector",
#     class_name="Warrior",
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory="Sword of Troy, Shield of Protection",
# )
#
# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
#
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)














