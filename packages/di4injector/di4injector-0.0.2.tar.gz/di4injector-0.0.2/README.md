# di4injector
DI for Injector

## How to use

```shell
pip install di4injector
```

```python
# at example.py

import abc
from di import DIContainer, DI


class GreetingService(abc.ABC):
    @abc.abstractmethod
    def greeting(self) -> str:
        pass

    
class EnglishGreetingService(GreetingService):
    def greeting(self) -> str:
        return 'Hello'


class JapaneseGreetingService(GreetingService):
    def greeting(self) -> str:
        return 'こんにちは'


di = DI.of(
    GreetingService,  # Abstract class 
    {  # inject
        "JP": JapaneseGreetingService,  # DI_PROFILE_ACTIVES=JP,...  
        "EN": EnglishGreetingService    # DI_PROFILE_ACTIVES=EN,...
    }, 
    EnglishGreetingService  # Default
)

DIContainer.instance().register(di)

greeting_service = DIContainer.instance().resolve(GreetingService)
greeting_service.greeting()
```

## For Developer

<details><summary>run test</summary>

```shell
pytest -v ./tests
```
</details>