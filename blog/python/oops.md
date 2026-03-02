---
layout: default
---

# Python Object-Oriented Programming Notes

## 📚 Table of Contents

1. [Classes and Objects](#classes-and-objects)
2. [Encapsulation and Access Modifiers](#encapsulation-and-access-modifiers)
3. [Properties (Getters and Setters)](#properties-getters-and-setters)
4. [Class Attributes and Class Methods](#class-attributes-and-class-methods)
   - 4.1 [Class Attribute](#class-attribute)
   - 4.2 [Class Method](#class-method)
5. [Static Methods](#static-methods)
6. [Inheritance](#inheritance)
   - 6.1 [Method Overriding](#method-overriding)
   - 6.2 [Using `super()`](#using-super)
7. [Multiple Inheritance](#multiple-inheritance)
8. [Polymorphism](#polymorphism)
9. [Method Overloading (Pythonic Style)](#method-overloading-pythonic-style)
10. [Abstraction](#abstraction)
11. [Style Guide and Further Reading](#style-guide-and-further-reading)
12. [🎯 Quick Reference Summary](#-quick-reference-summary)

---

## Classes and Objects

A class is a blueprint for creating objects.

Basic syntax:

```python
class SuperHero:
    def __init__(self, name: str, power: str, health: int, speed: int):
        self.name = name
        self.power = power
        self.health = health
        self.speed = speed
```

`__init__` is a special method that creates an object and initializes its attributes. It sets up the initial state of the object. 

Name convention: each word in the class name starts with a capital letter (no underscores).

An object is an instance of a class. 

```python
# Creating superhero objects
iron_man = SuperHero("Iron Man", "repulsor beams", 100, 80)
spider_man = SuperHero("Spider Man", "web slinging", 90, 95)
```

Object attributes are properties that belong to the object. 

Object methods are functions that belong to a class/object. Methods are functions that are defined inside a class. A function defined outside a class is not a method. 

Docstrings describe functions, methods, and classes and serve as documentation for your code. 

## Encapsulation and Access Modifiers

```python
class SuperHero:
    def __init__(self, name: str, power_level: int, public_name: str):
        self._name = name                # protected attribute
        self._power_level = power_level  # protected attribute
        self.public_name = public_name   # public attribute

    def get_name(self) -> str:           # public method
        return self._name
    
    def _some_protected_method(self) -> None:  # protected method
        pass
```

- **To access protected attributes, use public methods.**  
- **To access protected methods, use public methods.**

Child classes can access protected attributes/methods.

```python
class SuperHero:
    def __init__(self, name: str, power_level: int):
        self.__name = name                # private attribute
        self.__power_level = power_level  # private attribute

    # private method
    def __secret_power(self) -> str:
        return f"Using {self.__name}'s secret power!"
```

Private is a stronger form of encapsulation and can’t be accessed via a child class. It can only be accessed within the class. 

## Properties (Getters and Setters)

A getter is a method that returns a private/protected attribute. A setter is a method that sets the value of a private/protected attribute. 

The idiomatic way to use getter and setter methods is with the `@property` and `@<name>.setter` decorators. 

```python
class Hero:
    def __init__(self, name: str):
        self.__name = name    # private attribute

    # Getter
    @property
    def name(self) -> str:
        return self.__name

    # Setter
    @name.setter
    def name(self, new_name: str) -> None:
        if new_name != "":
            self.__name = new_name
        else:
            print("Name cannot be empty!")
            
hero = Hero("Batman")

# Getting name
print(hero.name)        # this calls the getter method, not the attribute
# Setting name
hero.name = "Superman"  # this calls the setter method, not the attribute
hero.name = ""          # Error: Name cannot be empty!
```

`@property` and the corresponding setter make code look cleaner and feel more natural to use. 

## Class Attributes and Class Methods

### Class Attribute

```python
class Superhero:
    hero_count = 0      # Class attribute

    def __init__(self, name: str, power: str):
        self.name = name      # Instance attribute
        self.power = power    # Instance attribute
        Superhero.hero_count += 1
```

### Class Method

```python
class Superhero:
    training_level = 1  # Class attribute

    def __init__(self, name: str, power: str):
        self.name = name         # Instance attribute
        self.power = power       # Instance attribute

    @classmethod
    def upgrade_training(cls) -> None:
        cls.training_level += 1
        print(f"All heroes now at training level {cls.training_level}")
        
Superhero.upgrade_training()     # Recommended way to use class method
print(Superhero.training_level)  # 2
```

Class methods don’t have access to instance attributes.  
Class methods can be defined with additional parameters after the `cls` parameter.

## Static Methods

```python
class Superhero:
    def __init__(self, name: str, power: str):
        if not self.is_valid_power(power):
            raise ValueError(f"Invalid power: {power}")
        self.name = name        # Instance attribute
        self.power = power      # Instance attribute

    @staticmethod
    def is_valid_power(power: str) -> bool:
        valid_powers = ["Flying", "Strength", "Speed", "Intelligence"]
        for valid_power in valid_powers:  # Iterate over each valid power and check if the power matches
            if power == valid_power:
                return True
        return False
```

Static methods are similar to class methods but:

- don’t have access to `self` or `cls`  
- can access class attributes (if referenced explicitly) but not instance attributes  
- are regular functions that live inside a class for organization purposes

## Inheritance

**Inheritance allows us to create a new class based on an existing class. The new class is known as a child class/subclass.** 

```python
class Superhero:
    def __init__(self, name: str, power: str):
        self.name = name
        self.power = power
        
class Avenger(Superhero):
    def fly(self) -> None:
        print(f"{self.name} can fly using {self.power}")
        
iron_man = Avenger("Iron Man", "repulsor beams")
iron_man.fly()  # Iron Man can fly using repulsor beams
```

### Method Overriding

```python
class Superhero:
    def __init__(self, name: str):
        self.name = name

    def fight(self) -> None:
        print("Superhero fights with advanced weapons!")

class Avenger(Superhero):
    # Override the fight method
    def fight(self) -> None:
        print("Avenger fights with advanced weapons!")
        
avenger = Avenger("Iron Man")
avenger.fight()  # Output: Avenger fights with advanced weapons!
```

### Using `super()`

`super()` extends parent class behavior. We can access parent class methods and properties:

```python
class ParentClass:
    def parent_method(self) -> None:
        print("This is the parent class method")

class ChildClass(ParentClass):
    def __init__(self) -> None:
        super().__init__()       # Call parent class __init__ (if defined)

    def child_method(self) -> None:
        super().parent_method()  # Call parent class's instance method
        print("This is the child class method")
```

## Multiple Inheritance

Multiple inheritance means a class can inherit from more than one parent class. 

```python
class Swimmer:
    def swim(self):
        print("Swimming")

class Flyer:
    def fly(self):
        print("Flying")

# Duck inherits from both Swimmer and Flyer
class Duck(Swimmer, Flyer):
    pass
    
duck = Duck()
duck.swim()  # Should print "Swimming"
duck.fly()   # Should print "Flying"
```

## Polymorphism

Polymorphism means "many forms" — the same interface, different implementations.

```python
class Superhero:
    def __init__(self, name: str, power: str):
        self.name = name
        self.power = power

    def special_power(self) -> None:
        pass  # Not needed for this example

class IronMan(Superhero):
    def special_power(self) -> None:
        print(f"{self.name} uses {self.power}")

class Thor(Superhero):
    def special_power(self) -> None:
        print(f"{self.name} uses {self.power}")

def display_power(hero: Superhero) -> None:
    hero.special_power()

iron_man = IronMan("Iron Man", "repulsor beams")
thor = Thor("Thor", "hammer")

display_power(iron_man)  # Iron Man uses repulsor beams
display_power(thor)      # Thor uses hammer
```

## Method Overloading (Pythonic Style)

Method overloading is having multiple behaviors for a method name, based on arguments.
In Python, this is usually done with default arguments or variable-length arguments.

```python
class Calculator:
    # Method 1: Default arguments
    def add(self, a: int, b: int, c: int = 0) -> int:
        return a + b + c

    # Method 2: Variable-length arguments
    def add_multiple(self, *args: int) -> int:
        return sum(args)
```

## Abstraction

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def query(self, sql: str) -> list:
        pass
```

Abstraction forces subclasses to implement abstract methods. If not implemented, it will throw an error when you try to instantiate the subclass. 

## Style Guide and Further Reading

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Python PEP 8](https://peps.python.org/pep-0008/)
- [Clean Code in Python](https://testdriven.io/blog/clean-code-python/)

---

## 🎯 Quick Reference Summary

| Concept | Key Points | Use When |
|---------|------------|----------|
| **Classes** | Blueprint for objects, use PascalCase | Creating reusable object templates |
| **Encapsulation** | `public`, `_protected`, `__private` | Controlling access to data |
| **Properties** | `@property` and `@setter` decorators | Need validation or computed attributes |
| **Inheritance** | `class Child(Parent):` | Extending existing functionality |
| **Polymorphism** | Same interface, different implementations | Code that works with multiple types |
| **Abstraction** | `@abstractmethod` from ABC | Enforcing implementation contracts |

---

> **💡 Pro Tip**: Start with simple classes and gradually add complexity. Focus on clear, descriptive names and keep methods focused on a single responsibility.
