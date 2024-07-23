# Brazil Municipal Holidays

A Python library to manage municipal holidays in the cities of Juiz de Fora, Coronel Fabriciano, Ipatinga and Governador Valadares. This library allows users to check, create, delete and manipulate holidays, including marking non-mandatory holidays as mandatory and vice versa.

## Functionalities
- Check holidays: Retrieve holidays for specific cities.
- Create holidays: Add new holidays to the city's list of holidays.
- Delete Holidays: Remove holidays from the city's holiday list.
- Check optional holidays: Identify which holidays are optional.
- Manipulate holidays: Change the status of holidays from non-mandatory to mandatory and vice versa.

## Installation
You can install the library using pip:
```pip install feriados-municipios```

## How to use
Here are some examples to get you started:

Importing the Library
```from feriados_municipios import *```

## Initialize Variables

```
import feriados_municipios
from datetime import date

hoje = date.today()

feriados_municipios.FeriadosBrasil(hoje)
feriados_municipios.FeriadosBrasil.Ipatinga.init()

print(feriados_municipios.FeriadosBrasil.Ipatinga.get_feriados_regionais())
```

## Add a New Holiday to the List for a Specified City
```FeriadosBrasil.Ipatinga.new_feriado_personalizado(day=1, month=2, name="Example Holiday", facultativo=False)```

## Check if the Date and Holiday
```FeriadosBrasil.Ipatinga.is_feriado()```

## Set a Holiday as Optional
```FeriadosBrasil.Ipatinga.set_feriado_as_facultativo_by_date(20, 7)```

## Get Optional Holidays from a Municipality
```FeriadosBrasil.Ipatinga.get_feriados_facultativos()```

## Remove a Holiday
```FeriadosBrasil.Ipatinga.del_feriado_by_date(20, 7)```

## Contributions
We accept contributions! Please read our contributing guidelines for more information.

## License
This project is licensed under the MIT License - see the LICENSE file for more details.

Feel free to modify this template to better suit the specifics and structure of your library.