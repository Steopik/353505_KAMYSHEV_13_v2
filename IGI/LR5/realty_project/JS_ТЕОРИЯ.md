# ТЕОРИЯ JAVASCRIPT - Полный справочник

**Автор**: Камышев
**Группа**: 353505
**Дата**: 2025

---

## Содержание

1. [Основы JavaScript](#1-основы-javascript)
2. [Переменные и типы данных](#2-переменные-и-типы-данных)
3. [Операторы](#3-операторы)
4. [Условия и циклы](#4-условия-и-циклы)
5. [Функции](#5-функции)
6. [Объекты и массивы](#6-объекты-и-массивы)
7. [ES6+ классы и ООП](#7-es6-классы-и-ооп)
8. [DOM манипуляции](#8-dom-манипуляции)
9. [События (Events)](#9-события-events)
10. [Асинхронное программирование](#10-асинхронное-программирование)
11. [Web Storage API](#11-web-storage-api)
12. [Современные Browser API](#12-современные-browser-api)
13. [Работа с JSON](#13-работа-с-json)
14. [Регулярные выражения](#14-регулярные-выражения)
15. [Продвинутые темы](#15-продвинутые-темы)

---

## 1. Основы JavaScript

### Что такое JavaScript?

JavaScript - это высокоуровневый, интерпретируемый язык программирования, который используется для создания интерактивных веб-страниц.

**Особенности:**
- Динамическая типизация
- Прототипное наследование
- Функции первого класса
- Однопоточный с event loop
- Выполняется в браузере или на сервере (Node.js)

### Подключение JavaScript

```html
<!-- Внутри HTML -->
<script>
    console.log('Hello World');
</script>

<!-- Внешний файл -->
<script src="script.js"></script>

<!-- С атрибутом defer (загрузка после парсинга HTML) -->
<script src="script.js" defer></script>

<!-- С атрибутом async (асинхронная загрузка) -->
<script src="script.js" async></script>
```

### Вывод в консоль

```javascript
console.log('Обычное сообщение');
console.error('Ошибка');
console.warn('Предупреждение');
console.info('Информация');
console.table([{name: 'John', age: 30}]); // Таблица
console.clear(); // Очистить консоль
```

---

## 2. Переменные и типы данных

### Объявление переменных

```javascript
// var - старый способ (не рекомендуется)
var x = 10;

// let - для изменяемых переменных (ES6+)
let name = 'John';
name = 'Jane'; // Можно изменить

// const - для констант (ES6+)
const PI = 3.14;
// PI = 3.15; // Ошибка!
```

**Разница между let, const и var:**

| Свойство | var | let | const |
|----------|-----|-----|-------|
| Область видимости | Функциональная | Блочная | Блочная |
| Hoisting | Да (undefined) | Нет (TDZ) | Нет (TDZ) |
| Переопределение | Да | Нет | Нет |
| Изменение | Да | Да | Нет |

### Примитивные типы данных

```javascript
// 1. Number (числа)
let age = 25;
let price = 99.99;
let infinity = Infinity;
let notANumber = NaN;

// 2. String (строки)
let firstName = "John";
let lastName = 'Doe';
let template = `Hello ${firstName}`; // Шаблонные строки

// 3. Boolean (логический)
let isActive = true;
let isDeleted = false;

// 4. Undefined (неопределенный)
let undefinedVar;
console.log(undefinedVar); // undefined

// 5. Null (пустое значение)
let emptyValue = null;

// 6. Symbol (уникальный идентификатор, ES6)
let id = Symbol('id');

// 7. BigInt (большие числа, ES11)
let bigNumber = 123456789012345678901234567890n;
```

### Проверка типов

```javascript
typeof 42;              // "number"
typeof "text";          // "string"
typeof true;            // "boolean"
typeof undefined;       // "undefined"
typeof null;            // "object" (особенность JS)
typeof {};              // "object"
typeof [];              // "object" (массив - это объект)
typeof function() {};   // "function"

// Проверка массива
Array.isArray([1, 2, 3]);  // true
Array.isArray({});         // false
```

### Преобразование типов

```javascript
// В строку
String(123);        // "123"
(123).toString();   // "123"
123 + "";           // "123"

// В число
Number("123");      // 123
parseInt("123px");  // 123
parseFloat("3.14"); // 3.14
+"123";             // 123

// В булев тип
Boolean(1);         // true
Boolean(0);         // false
Boolean("");        // false
Boolean("text");    // true
!!value;            // Преобразование в boolean
```

**Falsy значения** (приводятся к false):
- `false`
- `0`
- `""` (пустая строка)
- `null`
- `undefined`
- `NaN`

---

## 3. Операторы

### Арифметические операторы

```javascript
let a = 10, b = 3;

a + b;    // 13 (сложение)
a - b;    // 7  (вычитание)
a * b;    // 30 (умножение)
a / b;    // 3.333... (деление)
a % b;    // 1  (остаток от деления)
a ** b;   // 1000 (возведение в степень, ES7)

// Инкремент и декремент
let x = 5;
x++;      // 6 (постфиксный инкремент)
++x;      // 7 (префиксный инкремент)
x--;      // 6 (постфиксный декремент)
--x;      // 5 (префиксный декремент)
```

### Операторы сравнения

```javascript
5 == "5";   // true  (нестрогое равенство, с приведением типов)
5 === "5";  // false (строгое равенство, без приведения типов)

5 != "6";   // true  (нестрогое неравенство)
5 !== "5";  // true  (строгое неравенство)

5 > 3;      // true
5 < 3;      // false
5 >= 5;     // true
5 <= 4;     // false
```

**Правило:** Всегда используйте `===` и `!==` вместо `==` и `!=`!

### Логические операторы

```javascript
// && (И) - все должны быть true
true && true;   // true
true && false;  // false

// || (ИЛИ) - хотя бы один true
true || false;  // true
false || false; // false

// ! (НЕ) - инверсия
!true;   // false
!false;  // true

// Оператор нулевого слияния (ES11)
let value = null;
let result = value ?? "default";  // "default"
```

### Тернарный оператор

```javascript
// Синтаксис: условие ? значение_если_true : значение_если_false
let age = 18;
let status = age >= 18 ? "Совершеннолетний" : "Несовершеннолетний";

// Можно вкладывать
let result = age < 13 ? "Ребенок"
           : age < 18 ? "Подросток"
           : "Взрослый";
```

### Оператор spread (...)

```javascript
// Для массивов
let arr1 = [1, 2, 3];
let arr2 = [...arr1, 4, 5];  // [1, 2, 3, 4, 5]

// Для объектов
let obj1 = { a: 1, b: 2 };
let obj2 = { ...obj1, c: 3 };  // { a: 1, b: 2, c: 3 }

// Копирование массива
let copy = [...arr1];

// Объединение массивов
let merged = [...arr1, ...arr2];
```

### Деструктуризация

```javascript
// Массивы
let [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Объекты
let person = { name: 'John', age: 30, city: 'Minsk' };
let { name, age } = person;
// name = 'John', age = 30

// С переименованием
let { name: firstName, age: userAge } = person;

// Значения по умолчанию
let { country = 'Belarus' } = person;
```

---

## 4. Условия и циклы

### Условный оператор if-else

```javascript
let age = 20;

if (age < 18) {
    console.log("Несовершеннолетний");
} else if (age >= 18 && age < 65) {
    console.log("Взрослый");
} else {
    console.log("Пенсионер");
}
```

### Switch-case

```javascript
let day = 3;

switch (day) {
    case 1:
        console.log("Понедельник");
        break;
    case 2:
        console.log("Вторник");
        break;
    case 3:
        console.log("Среда");
        break;
    default:
        console.log("Другой день");
}
```

### Цикл for

```javascript
// Классический for
for (let i = 0; i < 5; i++) {
    console.log(i);  // 0, 1, 2, 3, 4
}

// for...of - для итерируемых объектов (массивы, строки)
let arr = [10, 20, 30];
for (let value of arr) {
    console.log(value);  // 10, 20, 30
}

// for...in - для перебора ключей объекта
let obj = { a: 1, b: 2, c: 3 };
for (let key in obj) {
    console.log(key, obj[key]);  // a 1, b 2, c 3
}
```

### Цикл while

```javascript
// while
let i = 0;
while (i < 5) {
    console.log(i);
    i++;
}

// do...while (выполнится хотя бы один раз)
let j = 0;
do {
    console.log(j);
    j++;
} while (j < 5);
```

### Управление циклами

```javascript
// break - выход из цикла
for (let i = 0; i < 10; i++) {
    if (i === 5) break;
    console.log(i);  // 0, 1, 2, 3, 4
}

// continue - пропуск итерации
for (let i = 0; i < 5; i++) {
    if (i === 2) continue;
    console.log(i);  // 0, 1, 3, 4
}
```

---

## 5. Функции

### Объявление функций

```javascript
// 1. Function Declaration (объявление функции)
function greet(name) {
    return `Hello, ${name}!`;
}

// 2. Function Expression (функциональное выражение)
const greet2 = function(name) {
    return `Hello, ${name}!`;
};

// 3. Arrow Function (стрелочная функция, ES6)
const greet3 = (name) => {
    return `Hello, ${name}!`;
};

// Короткий синтаксис для одной строки
const greet4 = name => `Hello, ${name}!`;

// Без параметров
const sayHello = () => console.log("Hello!");

// Несколько параметров
const sum = (a, b) => a + b;
```

### Параметры функции

```javascript
// Значения по умолчанию
function greet(name = "Guest") {
    return `Hello, ${name}!`;
}

// Rest параметры (собрать все в массив)
function sum(...numbers) {
    return numbers.reduce((acc, num) => acc + num, 0);
}
sum(1, 2, 3, 4);  // 10

// Деструктуризация параметров
function printPerson({ name, age }) {
    console.log(`${name} is ${age} years old`);
}
printPerson({ name: 'John', age: 30 });
```

### Возврат значений

```javascript
function calculate(a, b) {
    return {
        sum: a + b,
        diff: a - b,
        product: a * b
    };
}

let result = calculate(10, 5);
console.log(result.sum);  // 15
```

### Колбэк функции

```javascript
// Функция, которая принимает другую функцию
function processArray(arr, callback) {
    let result = [];
    for (let item of arr) {
        result.push(callback(item));
    }
    return result;
}

let numbers = [1, 2, 3, 4];
let doubled = processArray(numbers, x => x * 2);
// [2, 4, 6, 8]
```

### IIFE (Immediately Invoked Function Expression)

```javascript
// Немедленно вызываемая функция
(function() {
    console.log("Я выполнился сразу!");
})();

// Со стрелочной функцией
(() => {
    console.log("IIFE со стрелкой");
})();
```

### Области видимости (Scope)

```javascript
// Глобальная область
let globalVar = "Я глобальная";

function myFunction() {
    // Локальная область функции
    let localVar = "Я локальная";

    if (true) {
        // Блочная область
        let blockVar = "Я блочная";
        console.log(globalVar);  // Доступна
        console.log(localVar);   // Доступна
        console.log(blockVar);   // Доступна
    }

    // console.log(blockVar);  // Ошибка! Недоступна
}
```

---

## 6. Объекты и массивы

### Объекты

```javascript
// Создание объекта
let person = {
    name: 'John',
    age: 30,
    city: 'Minsk',
    isActive: true,

    // Метод объекта
    greet: function() {
        return `Hello, I'm ${this.name}`;
    },

    // Короткий синтаксис метода (ES6)
    sayHi() {
        return `Hi from ${this.name}`;
    }
};

// Доступ к свойствам
console.log(person.name);        // "John"
console.log(person['age']);      // 30
person.city = 'Brest';           // Изменение
person.country = 'Belarus';      // Добавление нового свойства

// Удаление свойства
delete person.isActive;

// Проверка наличия свойства
'name' in person;                // true
person.hasOwnProperty('name');   // true

// Получение ключей, значений, записей
Object.keys(person);             // ['name', 'age', 'city', ...]
Object.values(person);           // ['John', 30, 'Brest', ...]
Object.entries(person);          // [['name', 'John'], ['age', 30], ...]
```

### Массивы

```javascript
// Создание массива
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, 'text', true, null, { key: 'value' }];

// Доступ к элементам
console.log(numbers[0]);    // 1 (первый элемент)
console.log(numbers[numbers.length - 1]);  // 5 (последний)

// Длина массива
console.log(numbers.length);  // 5

// Изменение элемента
numbers[0] = 10;

// Многомерные массивы
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];
console.log(matrix[1][2]);  // 6
```

### Методы массивов

```javascript
let arr = [1, 2, 3, 4, 5];

// Добавление/удаление элементов
arr.push(6);        // Добавить в конец → [1,2,3,4,5,6]
arr.pop();          // Удалить с конца → [1,2,3,4,5]
arr.unshift(0);     // Добавить в начало → [0,1,2,3,4,5]
arr.shift();        // Удалить с начала → [1,2,3,4,5]

// splice(index, deleteCount, items...)
arr.splice(2, 1);   // Удалить 1 элемент с индекса 2 → [1,2,4,5]
arr.splice(1, 0, 99); // Вставить 99 на индекс 1 → [1,99,2,4,5]

// slice(start, end) - копирование части массива
let copy = arr.slice(1, 3);  // [99, 2]

// concat - объединение массивов
let arr2 = [6, 7, 8];
let combined = arr.concat(arr2);

// Поиск элементов
arr.indexOf(2);     // Индекс первого вхождения
arr.lastIndexOf(2); // Индекс последнего вхождения
arr.includes(3);    // true/false - есть ли элемент

// find - найти первый элемент, удовлетворяющий условию
let found = arr.find(x => x > 3);  // 4

// findIndex - найти индекс первого элемента
let index = arr.findIndex(x => x > 3);  // индекс элемента 4

// Сортировка
arr.sort();                    // Сортировка как строк
arr.sort((a, b) => a - b);     // Числовая сортировка по возрастанию
arr.sort((a, b) => b - a);     // По убыванию

// Разворот массива
arr.reverse();

// join - объединить в строку
arr.join(', ');  // "1, 2, 3, 4, 5"
```

### Функциональные методы массивов

```javascript
let numbers = [1, 2, 3, 4, 5];

// forEach - перебор (не возвращает значение)
numbers.forEach((num, index) => {
    console.log(`${index}: ${num}`);
});

// map - преобразование каждого элемента
let doubled = numbers.map(x => x * 2);  // [2, 4, 6, 8, 10]

// filter - фильтрация элементов
let evens = numbers.filter(x => x % 2 === 0);  // [2, 4]

// reduce - сведение к одному значению
let sum = numbers.reduce((acc, x) => acc + x, 0);  // 15

// some - хотя бы один элемент удовлетворяет условию
let hasEven = numbers.some(x => x % 2 === 0);  // true

// every - все элементы удовлетворяют условию
let allPositive = numbers.every(x => x > 0);  // true

// Цепочка методов
let result = numbers
    .filter(x => x > 2)     // [3, 4, 5]
    .map(x => x * 2)        // [6, 8, 10]
    .reduce((a, b) => a + b, 0);  // 24
```

---

## 7. ES6+ классы и ООП

### Классы (ES6)

```javascript
// Определение класса
class Person {
    // Конструктор
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    // Метод класса
    greet() {
        return `Hello, I'm ${this.name}`;
    }

    // Геттер
    get info() {
        return `${this.name}, ${this.age} лет`;
    }

    // Сеттер
    set info(value) {
        let [name, age] = value.split(', ');
        this.name = name;
        this.age = parseInt(age);
    }

    // Статический метод (вызывается на классе, а не на экземпляре)
    static species() {
        return 'Homo Sapiens';
    }
}

// Создание экземпляра
let john = new Person('John', 30);
john.greet();  // "Hello, I'm John"
john.info;     // "John, 30 лет" (геттер)
john.info = 'Jane, 25';  // Использование сеттера

// Статический метод
Person.species();  // "Homo Sapiens"
```

### Наследование (extends, super)

```javascript
// Родительский класс
class Animal {
    constructor(name) {
        this.name = name;
    }

    speak() {
        return `${this.name} издает звук`;
    }
}

// Дочерний класс
class Dog extends Animal {
    constructor(name, breed) {
        super(name);  // Вызов конструктора родителя (ОБЯЗАТЕЛЬНО!)
        this.breed = breed;
    }

    // Переопределение метода
    speak() {
        return `${this.name} лает: Гав-гав!`;
    }

    // Новый метод
    getBreed() {
        return this.breed;
    }
}

let dog = new Dog('Барбос', 'Овчарка');
dog.speak();     // "Барбос лает: Гав-гав!"
dog.getBreed();  // "Овчарка"
```

### Прототипное наследование (старый способ)

```javascript
// Конструктор-функция
function Person(name, age) {
    this.name = name;
    this.age = age;
}

// Добавление метода в прототип
Person.prototype.greet = function() {
    return `Hello, I'm ${this.name}`;
};

// Создание экземпляра
let person = new Person('John', 30);
person.greet();  // "Hello, I'm John"

// Наследование через прототипы
function Student(name, age, university) {
    Person.call(this, name, age);  // Вызов родительского конструктора
    this.university = university;
}

// Настройка цепочки прототипов
Student.prototype = Object.create(Person.prototype);
Student.prototype.constructor = Student;

// Добавление метода
Student.prototype.study = function() {
    return `${this.name} учится в ${this.university}`;
};

let student = new Student('Jane', 20, 'БГУ');
student.greet();  // "Hello, I'm Jane" (унаследовано)
student.study();  // "Jane учится в БГУ"
```

### Приватные поля (ES2022)

```javascript
class BankAccount {
    #balance = 0;  // Приватное поле (с #)

    constructor(owner) {
        this.owner = owner;
    }

    deposit(amount) {
        this.#balance += amount;
    }

    getBalance() {
        return this.#balance;
    }
}

let account = new BankAccount('John');
account.deposit(100);
account.getBalance();  // 100
// account.#balance;   // Ошибка! Приватное поле недоступно снаружи
```

---

## 8. DOM манипуляции

### Поиск элементов

```javascript
// По ID
let element = document.getElementById('myId');

// По классу (возвращает HTMLCollection)
let elements = document.getElementsByClassName('myClass');

// По тегу
let divs = document.getElementsByTagName('div');

// Селекторы CSS (современный способ)
let element = document.querySelector('.myClass');    // Первый элемент
let elements = document.querySelectorAll('.myClass'); // Все элементы (NodeList)

// Специальные селекторы
document.body;          // <body>
document.head;          // <head>
document.documentElement; // <html>
```

### Изменение содержимого

```javascript
let div = document.querySelector('#myDiv');

// Текстовое содержимое (безопасно)
div.textContent = 'Новый текст';

// HTML содержимое (небезопасно, может быть XSS)
div.innerHTML = '<strong>Жирный текст</strong>';

// Внешний HTML (весь элемент)
div.outerHTML = '<p>Параграф вместо div</p>';
```

### Изменение атрибутов

```javascript
let img = document.querySelector('img');

// Получение атрибута
img.getAttribute('src');

// Установка атрибута
img.setAttribute('src', 'new-image.jpg');
img.setAttribute('alt', 'Описание картинки');

// Удаление атрибута
img.removeAttribute('alt');

// Прямой доступ к некоторым атрибутам
img.src = 'new-image.jpg';
img.alt = 'Описание';

// data-атрибуты
let div = document.querySelector('[data-id="123"]');
div.dataset.id;         // "123"
div.dataset.name = 'John';  // Установит data-name="John"
```

### Работа с классами

```javascript
let element = document.querySelector('.myElement');

// Добавить класс
element.classList.add('active');
element.classList.add('highlight', 'visible');  // Несколько

// Удалить класс
element.classList.remove('active');

// Переключить класс (toggle)
element.classList.toggle('hidden');  // Если есть - удалит, если нет - добавит

// Проверить наличие класса
element.classList.contains('active');  // true/false

// Заменить класс
element.classList.replace('old-class', 'new-class');
```

### Работа со стилями

```javascript
let div = document.querySelector('#myDiv');

// Инлайн стили (inline styles)
div.style.color = 'red';
div.style.backgroundColor = 'blue';  // Camel case!
div.style.fontSize = '20px';

// Получение вычисленных стилей
let styles = getComputedStyle(div);
styles.color;         // "rgb(255, 0, 0)"
styles.fontSize;      // "20px"

// Множественные стили через cssText
div.style.cssText = 'color: red; background: blue; font-size: 20px;';
```

### Создание и удаление элементов

```javascript
// Создание элемента
let newDiv = document.createElement('div');
newDiv.textContent = 'Я новый div';
newDiv.className = 'new-element';
newDiv.id = 'uniqueId';

// Добавление в DOM
document.body.appendChild(newDiv);       // В конец body
document.body.prepend(newDiv);           // В начало body
parent.insertBefore(newDiv, refChild);   // Перед refChild

// Современные методы вставки (ES6)
element.append(newDiv);                  // В конец
element.prepend(newDiv);                 // В начало
element.before(newDiv);                  // До элемента
element.after(newDiv);                   // После элемента

// Удаление элемента
element.remove();                        // Современный способ
parent.removeChild(element);             // Старый способ

// Замена элемента
parent.replaceChild(newElement, oldElement);
element.replaceWith(newElement);         // Современный способ

// Клонирование элемента
let clone = element.cloneNode(true);     // true = глубокое клонирование
```

### Навигация по DOM

```javascript
let element = document.querySelector('#myElement');

// Родитель
element.parentElement;
element.parentNode;

// Дети
element.children;           // HTMLCollection (только элементы)
element.childNodes;         // NodeList (все ноды, включая текст)
element.firstElementChild;
element.lastElementChild;

// Соседи
element.nextElementSibling;
element.previousElementSibling;

// Проверка родителя
element.closest('.parent-class');  // Ближайший родитель с классом
```

---

## 9. События (Events)

### Добавление обработчиков событий

```javascript
let button = document.querySelector('#myButton');

// addEventListener (рекомендуется)
button.addEventListener('click', function(event) {
    console.log('Кнопка нажата!');
});

// Стрелочная функция
button.addEventListener('click', (event) => {
    console.log('Кнопка нажата!');
});

// Именованная функция
function handleClick(event) {
    console.log('Обработка клика');
}
button.addEventListener('click', handleClick);

// Удаление обработчика
button.removeEventListener('click', handleClick);
```

### Типы событий

```javascript
// Мышь
element.addEventListener('click', handler);       // Клик
element.addEventListener('dblclick', handler);    // Двойной клик
element.addEventListener('mouseenter', handler);  // Вход мыши
element.addEventListener('mouseleave', handler);  // Выход мыши
element.addEventListener('mousemove', handler);   // Движение мыши
element.addEventListener('mousedown', handler);   // Нажатие кнопки мыши
element.addEventListener('mouseup', handler);     // Отпускание кнопки мыши

// Клавиатура
element.addEventListener('keydown', handler);     // Нажатие клавиши
element.addEventListener('keyup', handler);       // Отпускание клавиши
element.addEventListener('keypress', handler);    // Нажатие символьной клавиши

// Формы
form.addEventListener('submit', handler);         // Отправка формы
input.addEventListener('input', handler);         // Ввод в поле
input.addEventListener('change', handler);        // Изменение значения
input.addEventListener('focus', handler);         // Фокус на элементе
input.addEventListener('blur', handler);          // Потеря фокуса

// Окно
window.addEventListener('load', handler);         // Полная загрузка страницы
window.addEventListener('DOMContentLoaded', handler); // DOM готов
window.addEventListener('resize', handler);       // Изменение размера окна
window.addEventListener('scroll', handler);       // Прокрутка
window.addEventListener('beforeunload', handler); // Перед закрытием
```

### Объект события (Event)

```javascript
element.addEventListener('click', function(event) {
    // Целевой элемент
    console.log(event.target);        // Элемент, на котором произошло событие
    console.log(event.currentTarget); // Элемент, на который повешен обработчик

    // Тип события
    console.log(event.type);          // "click"

    // Координаты мыши
    console.log(event.clientX, event.clientY);  // Относительно окна
    console.log(event.pageX, event.pageY);      // Относительно документа

    // Клавиши-модификаторы
    console.log(event.ctrlKey);   // Нажат Ctrl
    console.log(event.shiftKey);  // Нажат Shift
    console.log(event.altKey);    // Нажат Alt

    // Предотвращение действия по умолчанию
    event.preventDefault();

    // Остановка всплытия
    event.stopPropagation();
});
```

### События клавиатуры

```javascript
document.addEventListener('keydown', function(event) {
    console.log(event.key);        // Название клавиши: "a", "Enter", "ArrowLeft"
    console.log(event.code);       // Физический код: "KeyA", "Enter", "ArrowLeft"
    console.log(event.keyCode);    // Числовой код (устарело)

    // Проверка конкретной клавиши
    if (event.key === 'Enter') {
        console.log('Нажат Enter');
    }

    if (event.key === 'ArrowLeft') {
        console.log('Нажата стрелка влево');
    }

    // Комбинации клавиш
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault();  // Отменить Ctrl+S
        console.log('Сохранение...');
    }
});
```

### Делегирование событий

```javascript
// Вместо навешивания обработчика на каждый элемент...
// Вешаем один обработчик на родителя
document.querySelector('#parent').addEventListener('click', function(event) {
    // Проверяем, что кликнули именно по нужному элементу
    if (event.target.matches('.child-button')) {
        console.log('Кликнули по кнопке:', event.target.textContent);
    }
});

// Пример с таблицей
document.querySelector('#myTable').addEventListener('click', function(event) {
    // Найти ближайший <td>
    let td = event.target.closest('td');
    if (td && this.contains(td)) {
        console.log('Кликнули на ячейку:', td.textContent);
    }
});
```

### Пользовательские события

```javascript
// Создание пользовательского события
let customEvent = new CustomEvent('myEvent', {
    detail: { message: 'Привет!' },
    bubbles: true,
    cancelable: true
});

// Отправка события
element.dispatchEvent(customEvent);

// Прослушивание события
element.addEventListener('myEvent', function(event) {
    console.log(event.detail.message);  // "Привет!"
});
```

---

## 10. Асинхронное программирование

### setTimeout и setInterval

```javascript
// setTimeout - выполнить через N миллисекунд
setTimeout(function() {
    console.log('Прошла 1 секунда');
}, 1000);

// Со стрелочной функцией
setTimeout(() => {
    console.log('Прошло 2 секунды');
}, 2000);

// С параметрами
setTimeout((name) => {
    console.log(`Привет, ${name}!`);
}, 1000, 'John');

// Отмена таймера
let timerId = setTimeout(() => console.log('Никогда не выполнится'), 1000);
clearTimeout(timerId);

// setInterval - выполнять каждые N миллисекунд
let intervalId = setInterval(() => {
    console.log('Каждую секунду');
}, 1000);

// Остановка интервала
clearInterval(intervalId);
```

### Промисы (Promises)

```javascript
// Создание промиса
let promise = new Promise(function(resolve, reject) {
    // Асинхронная операция
    setTimeout(() => {
        let success = true;
        if (success) {
            resolve('Успех!');  // Промис выполнен
        } else {
            reject('Ошибка!');  // Промис отклонен
        }
    }, 1000);
});

// Обработка результата
promise
    .then(result => {
        console.log(result);  // "Успех!"
        return result + ' 2';
    })
    .then(result => {
        console.log(result);  // "Успех! 2"
    })
    .catch(error => {
        console.error(error);  // Если была ошибка
    })
    .finally(() => {
        console.log('Завершено');  // Выполнится в любом случае
    });

// Цепочка промисов
fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return fetch('/api/other');
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
```

### Async/Await (ES2017)

```javascript
// Async функция всегда возвращает промис
async function fetchData() {
    try {
        // await приостанавливает выполнение до получения результата
        let response = await fetch('/api/data');
        let data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Ошибка:', error);
        throw error;
    }
}

// Вызов async функции
fetchData()
    .then(data => console.log('Получены данные:', data))
    .catch(error => console.error('Ошибка:', error));

// Async со стрелочной функцией
const getData = async () => {
    let response = await fetch('/api/data');
    return await response.json();
};
```

### Promise методы

```javascript
// Promise.all - дождаться всех промисов
let promise1 = fetch('/api/users');
let promise2 = fetch('/api/posts');
let promise3 = fetch('/api/comments');

Promise.all([promise1, promise2, promise3])
    .then(([users, posts, comments]) => {
        console.log('Все данные получены');
    })
    .catch(error => {
        console.error('Хотя бы один промис отклонен');
    });

// Promise.race - первый выполненный промис
Promise.race([promise1, promise2, promise3])
    .then(result => {
        console.log('Первый результат:', result);
    });

// Promise.allSettled - дождаться всех (не важно, успех или ошибка)
Promise.allSettled([promise1, promise2, promise3])
    .then(results => {
        results.forEach((result, index) => {
            if (result.status === 'fulfilled') {
                console.log(`Промис ${index} выполнен:`, result.value);
            } else {
                console.log(`Промис ${index} отклонен:`, result.reason);
            }
        });
    });

// Promise.any - первый успешный промис
Promise.any([promise1, promise2, promise3])
    .then(result => {
        console.log('Первый успешный:', result);
    });
```

### Fetch API

```javascript
// GET запрос
fetch('https://api.example.com/data')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ошибка! Статус: ${response.status}`);
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error('Ошибка:', error));

// POST запрос
fetch('https://api.example.com/users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        name: 'John',
        email: 'john@example.com'
    })
})
    .then(response => response.json())
    .then(data => console.log('Создан пользователь:', data))
    .catch(error => console.error('Ошибка:', error));

// Async/Await версия
async function fetchUser(userId) {
    try {
        let response = await fetch(`https://api.example.com/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP ошибка! Статус: ${response.status}`);
        }
        let user = await response.json();
        return user;
    } catch (error) {
        console.error('Ошибка при загрузке пользователя:', error);
    }
}
```

---

## 11. Web Storage API

### localStorage

```javascript
// Сохранение данных (строки)
localStorage.setItem('username', 'John');
localStorage.setItem('theme', 'dark');

// Получение данных
let username = localStorage.getItem('username');  // "John"

// Удаление данных
localStorage.removeItem('username');

// Очистка всего хранилища
localStorage.clear();

// Проверка наличия ключа
if (localStorage.getItem('theme')) {
    console.log('Тема сохранена');
}

// Сохранение объектов (через JSON)
let user = { name: 'John', age: 30 };
localStorage.setItem('user', JSON.stringify(user));

// Получение объектов
let savedUser = JSON.parse(localStorage.getItem('user'));

// Количество записей
let count = localStorage.length;

// Получение ключа по индексу
let key = localStorage.key(0);

// Перебор всех записей
for (let i = 0; i < localStorage.length; i++) {
    let key = localStorage.key(i);
    let value = localStorage.getItem(key);
    console.log(`${key}: ${value}`);
}
```

### sessionStorage

```javascript
// Работает идентично localStorage, но данные хранятся
// только в течение сессии (до закрытия вкладки)

sessionStorage.setItem('tempData', 'Временные данные');
let data = sessionStorage.getItem('tempData');
sessionStorage.removeItem('tempData');
sessionStorage.clear();
```

**Разница между localStorage и sessionStorage:**

| localStorage | sessionStorage |
|--------------|----------------|
| Данные хранятся постоянно | Данные удаляются при закрытии вкладки |
| Доступны во всех вкладках одного домена | Доступны только в текущей вкладке |
| ~5-10 МБ | ~5-10 МБ |

---

## 12. Современные Browser API

### Intersection Observer API

```javascript
// Отслеживание появления элементов в области видимости
let observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            console.log('Элемент виден!');
            entry.target.classList.add('visible');
        } else {
            entry.target.classList.remove('visible');
        }
    });
}, {
    threshold: 0.5,      // 50% элемента должно быть видно
    rootMargin: '0px'    // Отступ от области видимости
});

// Начать наблюдение
let element = document.querySelector('.animate-on-scroll');
observer.observe(element);

// Прекратить наблюдение
observer.unobserve(element);
```

### Geolocation API

```javascript
// Получение координат пользователя
if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
        // Успех
        (position) => {
            let lat = position.coords.latitude;
            let lon = position.coords.longitude;
            console.log(`Координаты: ${lat}, ${lon}`);
        },
        // Ошибка
        (error) => {
            console.error('Ошибка геолокации:', error.message);
        },
        // Опции
        {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        }
    );
}
```

### Clipboard API

```javascript
// Копирование текста в буфер обмена
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        console.log('Текст скопирован!');
    } catch (error) {
        console.error('Ошибка копирования:', error);
    }
}

// Вставка из буфера обмена
async function pasteFromClipboard() {
    try {
        let text = await navigator.clipboard.readText();
        console.log('Вставленный текст:', text);
        return text;
    } catch (error) {
        console.error('Ошибка вставки:', error);
    }
}
```

### Battery Status API

```javascript
// Информация о батарее
if ('getBattery' in navigator) {
    navigator.getBattery().then((battery) => {
        console.log(`Уровень заряда: ${battery.level * 100}%`);
        console.log(`Заряжается: ${battery.charging}`);
        console.log(`Время до разрядки: ${battery.dischargingTime} сек`);

        // Отслеживание изменений
        battery.addEventListener('levelchange', () => {
            console.log(`Новый уровень: ${battery.level * 100}%`);
        });
    });
}
```

### Speech Synthesis API

```javascript
// Синтез речи (озвучивание текста)
if ('speechSynthesis' in window) {
    let utterance = new SpeechSynthesisUtterance('Привет, мир!');
    utterance.lang = 'ru-RU';
    utterance.rate = 1.0;    // Скорость (0.1 - 10)
    utterance.pitch = 1.0;   // Высота тона (0 - 2)
    utterance.volume = 1.0;  // Громкость (0 - 1)

    speechSynthesis.speak(utterance);

    // Остановка
    speechSynthesis.cancel();
}
```

### Blob API (сохранение файлов)

```javascript
// Создание и скачивание файла
function saveToFile(content, filename) {
    // Создаем Blob
    let blob = new Blob([content], { type: 'text/plain; charset=utf-8' });

    // Создаем ссылку для скачивания
    let link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;

    // Кликаем программно
    link.click();

    // Освобождаем память
    URL.revokeObjectURL(link.href);
}

saveToFile('Привет, мир!', 'hello.txt');
```

### Canvas API (работа с изображениями)

```javascript
let canvas = document.getElementById('myCanvas');
let ctx = canvas.getContext('2d');

// Сохранение canvas в файл
function saveCanvasToFile() {
    let link = document.createElement('a');
    link.download = 'canvas.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
}
```

---

## 13. Работа с JSON

### JSON.stringify()

```javascript
let obj = {
    name: 'John',
    age: 30,
    hobbies: ['coding', 'reading'],
    address: {
        city: 'Minsk',
        country: 'Belarus'
    }
};

// Преобразование в JSON строку
let json = JSON.stringify(obj);
// '{"name":"John","age":30,"hobbies":["coding","reading"],"address":{"city":"Minsk","country":"Belarus"}}'

// С форматированием (отступы)
let prettyJson = JSON.stringify(obj, null, 2);
/*
{
  "name": "John",
  "age": 30,
  "hobbies": [
    "coding",
    "reading"
  ],
  "address": {
    "city": "Minsk",
    "country": "Belarus"
  }
}
*/

// Фильтрация свойств
let filtered = JSON.stringify(obj, ['name', 'age']);
// '{"name":"John","age":30}'
```

### JSON.parse()

```javascript
let jsonString = '{"name":"John","age":30}';

// Парсинг JSON
let obj = JSON.parse(jsonString);
console.log(obj.name);  // "John"
console.log(obj.age);   // 30

// Обработка ошибок
try {
    let invalidJson = '{ invalid json }';
    let parsed = JSON.parse(invalidJson);
} catch (error) {
    console.error('Ошибка парсинга JSON:', error);
}
```

---

## 14. Регулярные выражения

### Создание регулярных выражений

```javascript
// Литеральная нотация
let regex1 = /pattern/flags;

// Конструктор
let regex2 = new RegExp('pattern', 'flags');

// Примеры
let emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
let phoneRegex = /^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$/;
```

### Флаги

```javascript
// g - глобальный поиск (все совпадения)
// i - регистронезависимый
// m - многострочный режим
// s - . соответствует переносу строки
// u - поддержка Unicode
// y - поиск с конкретной позиции

let regex = /hello/gi;  // Найти все "hello" без учета регистра
```

### Методы строк для работы с regex

```javascript
let text = "Hello World! Hello JavaScript!";

// match() - найти совпадения
text.match(/hello/i);     // ["Hello"]
text.match(/hello/gi);    // ["Hello", "Hello"]

// search() - найти позицию первого совпадения
text.search(/world/i);    // 6

// replace() - заменить
text.replace(/hello/i, 'Hi');        // "Hi World! Hello JavaScript!"
text.replace(/hello/gi, 'Hi');       // "Hi World! Hi JavaScript!"

// replaceAll() - заменить все (ES2021)
text.replaceAll('Hello', 'Hi');      // "Hi World! Hi JavaScript!"

// split() - разделить
"apple,banana,orange".split(/,/);    // ["apple", "banana", "orange"]
```

### Методы regex

```javascript
let regex = /\d+/g;  // Одна или более цифр
let text = "У меня 2 кота и 3 собаки";

// test() - проверка наличия
regex.test(text);    // true

// exec() - получить информацию о совпадении
let match;
while ((match = regex.exec(text)) !== null) {
    console.log(`Найдено ${match[0]} на позиции ${match.index}`);
}
// "Найдено 2 на позиции 7"
// "Найдено 3 на позиции 17"
```

### Паттерны

```javascript
// Символьные классы
/\d/      // Цифра (0-9)
/\D/      // Не цифра
/\w/      // Буква, цифра или _ (a-zA-Z0-9_)
/\W/      // Не буква/цифра/_
/\s/      // Пробельный символ (пробел, tab, \n)
/\S/      // Не пробельный символ
/./       // Любой символ кроме \n
/[abc]/   // Один из символов a, b или c
/[^abc]/  // Любой символ кроме a, b, c
/[a-z]/   // Любая строчная буква
/[A-Z]/   // Любая заглавная буква
/[0-9]/   // Любая цифра

// Квантификаторы
/a*/      // 0 или более "a"
/a+/      // 1 или более "a"
/a?/      // 0 или 1 "a"
/a{3}/    // Ровно 3 "a"
/a{2,5}/  // От 2 до 5 "a"
/a{2,}/   // 2 или более "a"

// Якоря
/^hello/  // Начало строки
/world$/  // Конец строки
/\b/      // Граница слова

// Группы
/(abc)/   // Группа захвата
/(?:abc)/ // Группа без захвата
/a|b/     // "a" или "b"
```

### Примеры валидации

```javascript
// Email
function isValidEmail(email) {
    let regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}

// Телефон (формат: +375 (29) 123-45-67)
function isValidPhone(phone) {
    let regex = /^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$/;
    return regex.test(phone);
}

// URL
function isValidURL(url) {
    let regex = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    return regex.test(url);
}

// Пароль (минимум 8 символов, буква и цифра)
function isStrongPassword(password) {
    let regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    return regex.test(password);
}
```

---

## 15. Продвинутые темы

### Замыкания (Closures)

```javascript
// Замыкание - функция, которая запоминает свое лексическое окружение
function makeCounter() {
    let count = 0;  // Локальная переменная

    return function() {
        count++;
        return count;
    };
}

let counter = makeCounter();
console.log(counter());  // 1
console.log(counter());  // 2
console.log(counter());  // 3

// Приватные переменные через замыкание
function createPerson(name) {
    let age = 0;  // Приватная переменная

    return {
        getName() {
            return name;
        },
        getAge() {
            return age;
        },
        setAge(newAge) {
            if (newAge > 0) age = newAge;
        }
    };
}

let person = createPerson('John');
person.getName();   // "John"
person.setAge(30);
person.getAge();    // 30
// person.age;      // undefined (нет прямого доступа)
```

### Контекст this

```javascript
let user = {
    name: 'John',
    greet: function() {
        console.log(`Hello, ${this.name}`);
    }
};

user.greet();  // "Hello, John"

// Потеря контекста
let greet = user.greet;
greet();  // "Hello, undefined" (this = window/undefined)

// Привязка контекста с bind()
let boundGreet = user.greet.bind(user);
boundGreet();  // "Hello, John"

// call() - вызов с явным контекстом
user.greet.call({ name: 'Jane' });  // "Hello, Jane"

// apply() - то же, но аргументы массивом
function introduce(greeting, punctuation) {
    console.log(`${greeting}, ${this.name}${punctuation}`);
}
introduce.apply(user, ['Hi', '!']);  // "Hi, John!"

// Стрелочные функции не имеют своего this
let obj = {
    name: 'John',
    delayedGreet: function() {
        setTimeout(() => {
            console.log(`Hello, ${this.name}`);  // this = obj
        }, 1000);
    }
};
```

### Модули (ES6)

```javascript
// file: math.js
export function sum(a, b) {
    return a + b;
}

export const PI = 3.14159;

export default class Calculator {
    add(a, b) {
        return a + b;
    }
}

// file: main.js
import Calculator, { sum, PI } from './math.js';
import * as Math from './math.js';  // Импорт всего

console.log(sum(2, 3));  // 5
console.log(PI);         // 3.14159

let calc = new Calculator();
calc.add(5, 10);  // 15
```

### Генераторы (Generators)

```javascript
// Функция-генератор
function* numberGenerator() {
    yield 1;
    yield 2;
    yield 3;
}

let gen = numberGenerator();
console.log(gen.next());  // { value: 1, done: false }
console.log(gen.next());  // { value: 2, done: false }
console.log(gen.next());  // { value: 3, done: false }
console.log(gen.next());  // { value: undefined, done: true }

// Бесконечный генератор
function* infiniteNumbers() {
    let i = 0;
    while (true) {
        yield i++;
    }
}

let infinite = infiniteNumbers();
console.log(infinite.next().value);  // 0
console.log(infinite.next().value);  // 1
```

### Символы (Symbols)

```javascript
// Уникальные идентификаторы
let id1 = Symbol('id');
let id2 = Symbol('id');
console.log(id1 === id2);  // false (каждый Symbol уникален)

// Скрытые свойства объекта
let user = {
    name: 'John',
    [id1]: 123  // Символьное свойство
};

console.log(user[id1]);  // 123
Object.keys(user);       // ["name"] (символы не попадают)
```

### Map и Set

```javascript
// Map - коллекция ключ-значение (ключи могут быть любого типа)
let map = new Map();
map.set('name', 'John');
map.set(1, 'number key');
map.set(true, 'boolean key');

map.get('name');   // "John"
map.has('name');   // true
map.delete('name');
map.size;          // 2
map.clear();       // Очистить все

// Перебор Map
for (let [key, value] of map) {
    console.log(`${key}: ${value}`);
}

// Set - коллекция уникальных значений
let set = new Set();
set.add(1);
set.add(2);
set.add(2);  // Дубликат, не добавится
set.add(3);

set.size;      // 3
set.has(2);    // true
set.delete(2);

// Преобразование массива в Set (удаление дубликатов)
let arr = [1, 2, 2, 3, 3, 4];
let unique = [...new Set(arr)];  // [1, 2, 3, 4]
```

### WeakMap и WeakSet

```javascript
// WeakMap - Map со слабыми ссылками на ключи (только объекты)
let weakMap = new WeakMap();
let obj = { name: 'John' };

weakMap.set(obj, 'metadata');
weakMap.get(obj);  // "metadata"

// Когда obj удалится, запись в WeakMap тоже удалится автоматически

// WeakSet - Set со слабыми ссылками
let weakSet = new WeakSet();
weakSet.add(obj);
weakSet.has(obj);  // true
```

### Proxy

```javascript
// Proxy - перехватчик операций над объектом
let target = {
    name: 'John',
    age: 30
};

let proxy = new Proxy(target, {
    get(target, prop) {
        console.log(`Чтение свойства ${prop}`);
        return target[prop];
    },
    set(target, prop, value) {
        console.log(`Запись ${value} в свойство ${prop}`);
        target[prop] = value;
        return true;
    }
});

proxy.name;       // "Чтение свойства name"
proxy.age = 31;   // "Запись 31 в свойство age"
```

### Debounce и Throttle

```javascript
// Debounce - выполнить функцию через N мс после последнего вызова
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// Использование: отложенный поиск при вводе
let searchInput = document.querySelector('#search');
let debouncedSearch = debounce(function(event) {
    console.log('Поиск:', event.target.value);
}, 500);
searchInput.addEventListener('input', debouncedSearch);

// Throttle - выполнять не чаще чем раз в N мс
function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
        let now = Date.now();
        if (now - lastCall >= delay) {
            lastCall = now;
            func.apply(this, args);
        }
    };
}

// Использование: ограничить частоту обработки скролла
let throttledScroll = throttle(function() {
    console.log('Скролл:', window.scrollY);
}, 200);
window.addEventListener('scroll', throttledScroll);
```

---

## Практические примеры из проекта

### Пример 1: Слайдер изображений (Класс)

```javascript
class Slider {
    constructor(options) {
        this.options = {
            container: '#slider',
            loop: true,
            auto: false,
            delay: 5,
            ...options
        };

        this.container = document.querySelector(this.options.container);
        this.slides = this.container.querySelectorAll('.slide');
        this.currentIndex = 0;
        this.autoplayInterval = null;

        this.init();
    }

    init() {
        this.setupNavigation();
        if (this.options.auto) {
            this.startAutoplay();
        }
        this.setupKeyboardNavigation();
    }

    next() {
        let nextIndex = this.currentIndex + 1;
        if (nextIndex >= this.slides.length) {
            nextIndex = this.options.loop ? 0 : this.currentIndex;
        }
        this.goToSlide(nextIndex);
    }

    prev() {
        let prevIndex = this.currentIndex - 1;
        if (prevIndex < 0) {
            prevIndex = this.options.loop ? this.slides.length - 1 : 0;
        }
        this.goToSlide(prevIndex);
    }

    goToSlide(index) {
        this.slides[this.currentIndex].classList.remove('active');
        this.currentIndex = index;
        this.slides[this.currentIndex].classList.add('active');
    }

    startAutoplay() {
        let delayMs = this.options.delay * 1000;
        this.autoplayInterval = setInterval(() => this.next(), delayMs);
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'ArrowRight') this.next();
        });
    }
}

// Использование
let slider = new Slider({
    container: '#mySlider',
    loop: true,
    auto: true,
    delay: 3
});
```

### Пример 2: Переключатель темы с LocalStorage

```javascript
class ThemeSwitcher {
    constructor() {
        this.STORAGE_KEY = 'preferred-theme';
        this.themes = {
            LIGHT: 'light',
            DARK: 'dark'
        };
        this.init();
    }

    getSavedTheme() {
        return localStorage.getItem(this.STORAGE_KEY) || this.themes.LIGHT;
    }

    saveTheme(theme) {
        localStorage.setItem(this.STORAGE_KEY, theme);
    }

    applyTheme(theme) {
        let html = document.documentElement;
        if (theme === this.themes.DARK) {
            html.classList.add('dark-theme');
            html.classList.remove('light-theme');
        } else {
            html.classList.add('light-theme');
            html.classList.remove('dark-theme');
        }
        html.setAttribute('data-theme', theme);
    }

    toggleTheme() {
        let currentTheme = this.getSavedTheme();
        let newTheme = currentTheme === this.themes.LIGHT
            ? this.themes.DARK
            : this.themes.LIGHT;

        this.applyTheme(newTheme);
        this.saveTheme(newTheme);
    }

    init() {
        let savedTheme = this.getSavedTheme();
        this.applyTheme(savedTheme);

        document.getElementById('theme-toggle')
            ?.addEventListener('change', () => this.toggleTheme());
    }
}
```

### Пример 3: Наследование классов (Spring Dates)

```javascript
// Базовый класс
class DateManager {
    constructor() {
        this.dates = [];
    }

    getDates() {
        return this.dates;
    }

    addDateFromForm(day, month, year) {
        this.dates.push({
            day: parseInt(day),
            month: parseInt(month),
            year: parseInt(year)
        });
    }

    formatDate(date) {
        let months = ['Январь', 'Февраль', 'Март', ...];
        return `${date.day} ${months[date.month - 1]} ${date.year}`;
    }
}

// Производный класс с extends
class SpringDateManager extends DateManager {
    constructor() {
        super();  // Вызов конструктора родителя
        this.springMonths = [3, 4, 5];  // Март, апрель, май
    }

    isSpringDate(date) {
        return this.springMonths.includes(date.month);
    }

    displaySpringDates(containerId) {
        let springDates = this.dates.filter(date => this.isSpringDate(date));
        // ... отображение в DOM
        return springDates;
    }

    saveSpringDatesToFile(filename) {
        let springDates = this.dates.filter(date => this.isSpringDate(date));
        let content = springDates.map(d => this.formatDate(d)).join('\n');

        let blob = new Blob([content], {type: 'text/plain; charset=utf-8'});
        let link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    }
}
```

### Пример 4: Intersection Observer (Анимация при скролле)

```javascript
class ScrollAnimations {
    constructor(options) {
        this.options = {
            threshold: 0.15,
            rootMargin: '0px',
            animateOnce: false,
            ...options
        };
        this.observer = null;
        this.init();
    }

    init() {
        if (!('IntersectionObserver' in window)) {
            console.warn('Intersection Observer не поддерживается');
            return;
        }

        this.observer = new IntersectionObserver(
            (entries) => this.handleIntersection(entries),
            {
                threshold: this.options.threshold,
                rootMargin: this.options.rootMargin
            }
        );

        this.observeElements();
    }

    observeElements() {
        let elements = document.querySelectorAll('[data-scroll]');
        elements.forEach(element => {
            element.style.opacity = '0';
            this.observer.observe(element);
        });
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.animateElement(entry.target);
                if (this.options.animateOnce) {
                    this.observer.unobserve(entry.target);
                }
            } else if (!this.options.animateOnce) {
                this.resetElement(entry.target);
            }
        });
    }

    animateElement(element) {
        let animationType = element.dataset.scroll || 'fade';
        element.style.opacity = '1';
        element.classList.add('scroll-animate');
        element.classList.add(`scroll-${animationType}`);
    }

    resetElement(element) {
        element.classList.remove('scroll-animate', 'scroll-animated');
        element.style.opacity = '0';
    }
}

// Использование
let scrollAnimations = new ScrollAnimations({
    threshold: 0.15,
    animateOnce: false
});
```

---

## Полезные ссылки

- **MDN Web Docs**: https://developer.mozilla.org/ru/docs/Web/JavaScript
- **JavaScript.info**: https://javascript.info/
- **Can I Use**: https://caniuse.com/ (проверка поддержки браузерами)
- **RegExr**: https://regexr.com/ (тестирование регулярных выражений)
- **Chart.js**: https://www.chartjs.org/
- **ES6 Features**: http://es6-features.org/

---

## Шпаргалка по методам

### Array методы

```javascript
// Мутирующие (изменяют исходный массив)
push(), pop(), shift(), unshift(), splice(), sort(), reverse()

// Не мутирующие (возвращают новый массив)
concat(), slice(), map(), filter(), reduce()

// Поиск
find(), findIndex(), indexOf(), includes(), some(), every()

// Перебор
forEach(), map(), filter(), reduce(), reduceRight()
```

### String методы

```javascript
// Поиск
indexOf(), lastIndexOf(), includes(), startsWith(), endsWith()

// Извлечение
slice(), substring(), substr()

// Изменение
toLowerCase(), toUpperCase(), trim(), trimStart(), trimEnd()

// Разделение/объединение
split(), concat()

// Замена
replace(), replaceAll()

// Проверка
match(), search(), test()
```

### Object методы

```javascript
Object.keys(obj)        // Массив ключей
Object.values(obj)      // Массив значений
Object.entries(obj)     // Массив пар [ключ, значение]
Object.assign(target, source)  // Копирование свойств
Object.freeze(obj)      // Заморозить объект
Object.seal(obj)        // Запечатать объект
```

---

**Конец справочника JavaScript**

© 2025 Камышев, Группа 353505
