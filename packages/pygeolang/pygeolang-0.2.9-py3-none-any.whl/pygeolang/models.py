from dataclasses import dataclass, field

@dataclass
class Country:
    name: str
    alpha_2: str
    alpha_3: str
    numeric: str
    official_name: str
    continent: str
    languages: list[str] = field(default_factory=list)

@dataclass
class Continent:
    name: str
    code: str
    countries: list[str] = field(default_factory=list)  # Store country names, not objects
