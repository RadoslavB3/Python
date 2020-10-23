from typing import List, Tuple, Optional


class Person:
    def __init__(self, name, born_year, eye_color):
        self.name = name
        self.born_year = born_year
        self.eye_color = eye_color
        self.parent = None
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def siblings(self):
        siblings = []
        if self.parent is None:
            return []
        for child in self.parent.children:
            if child != self:
                siblings.append(child)
        return siblings

    def siblings_eye_color(self):
        siblings = self.siblings()
        if siblings == []:
            return True
        color = siblings[0].eye_color
        for sibl in siblings:
            if sibl.eye_color != color:
                return False
        return True

    def validate_eye_color(self, color: str) -> bool:
        validation = True
        if self.children == []:
            return self.eye_color == color
        for child in self.children:
            validation = self.eye_color == color \
                         and validation and child.validate_eye_color(color)
        return validation

    def validate_children_min(self, color: str, count: int) -> bool:
        validation = True
        if self.eye_color == color and len(self.children) < count:
            return False
        for child in self.children:
            validation = validation \
                         and child.validate_children_min(color, count)
        return validation

    def draw_tree(self, level):
        print(("~" * level * 4) + self.name + " (" + str(self.born_year) + ")")
        for child in sorted(self.children, key=lambda x: x.born_year):
            child.draw_tree(level + 1)

    def draw_family_tree(self):
        self.draw_tree(0)

    def change_eye_color(self, old: str, new: str) -> None:
        if self.eye_color == old:
            self.eye_color = new
        for child in self.children:
            child.change_eye_color(old, new)

    def change_born_year(self, increment: int) -> None:
        if self.siblings_eye_color():
            self.born_year += increment
        for child in self.children:
            child.change_born_year(increment)

    def people_by_year(self, start: int, end: int) -> List['Person']:
        result = []
        if start <= self.born_year <= end:
            result.append(self)
        for child in self.children:
            result += child.people_by_year(start, end)
        return result

    def find_aunt(self, count):
        if self.parent is None:
            return False
        if len(self.parent.siblings()) == 0:
            return False
        for aunt in self.parent.siblings():
            if len(aunt.children) == count:
                return True
        return False

    def people_with_aunt_children(self, count: int) -> List['Person']:
        result = []
        if self.find_aunt(count):
            result.append(self)
        for child in self.children:
            result += child.people_with_aunt_children(count)
        return result

    def youngest_child(self):
        if self.children == []:
            return None
        youngest = self.children[0]
        for child in self.children:
            if child.born_year > youngest.born_year:
                youngest = child
        return youngest

    def mother_childbirth(self):
        if self.youngest_child() is not None:
            return self.youngest_child().born_year - self.born_year

    def oldest_mother_with_parameters(self, oldest_mum):
        if self.mother_childbirth() is not None and \
                self.mother_childbirth() > oldest_mum.mother_childbirth():
            oldest_mum = self
        for child in self.children:
            oldest_mum = child.oldest_mother_with_parameters(oldest_mum)
        return oldest_mum

    def oldest_mother(self) -> Optional['Person']:
        if self.children == []:
            return None
        return self.oldest_mother_with_parameters(self)

    def count_node(self):
        count = 0
        for child in self.children:
            count += 1 + child.count_node()
        return count

    def cut_years(self, start: int, end: int) -> int:
        count = 0
        if start <= self.born_year <= end and self.parent is None:
            return self.count_node() + 1
        if start <= self.born_year <= end:
            count += self.count_node() + 1
            self.parent.children = self.siblings()
        else:
            for child in self.children:
                count += child.cut_years(start, end)
        return count

    def validate_children_color(self, color):
        validation = True
        for child in self.children:
            validation = validation and child.validate_eye_color(color)
        return validation

    def people_to_cut(self, color):
        result = []
        if self.validate_children_color(color):
            result.append(self)
        for child in self.children:
            result += child.people_to_cut(color)
        return result

    def cut_subtree_parameters(self, color, root):
        people = self.people_to_cut(color)
        if self in people:
            self.parent.children = self.siblings()
            if root:
                return True
        for child in self.children:
            child.cut_subtree_parameters(color, False)
        return False

    def cut_subtree_color(self, color: str) -> bool:
        if self.validate_children_color(color) \
                and self.parent is None:
            return True
        return self.cut_subtree_parameters(color, True)

    def __str__(self):
        return "{} born in {} with {} eyes"\
            .format(self.name, self.born_year, self.eye_color)


def build_tree(persons: List[Tuple[str, int, str]],
               relations: List[Tuple[str, str]]) -> Optional['Person']:
    if persons == [] and relations == []:
        return None

    people = []
    for person in persons:
        name = person[0]
        born_year = person[1]
        eye_color = person[2]
        pupil = Person(name, born_year, eye_color)
        people.append(pupil)

    for relation in relations:
        found_child, found_parent = False, False
        for pupil in people:
            if relation[0] == pupil.name:
                parent = pupil
                found_parent = True
            if relation[1] == pupil.name:
                child = pupil
                found_child = True
        if found_parent and found_child:
            parent.add_child(child)

    for pupil in people:
        if pupil.parent is None:
            return pupil
