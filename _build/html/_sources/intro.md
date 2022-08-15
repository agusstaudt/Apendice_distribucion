# Apéndices del Libro Pobreza y Desigualdad en Python

*Bonavida, Cristian - CEDLAS*[^1]

*Laguinge, Luis - CEDLAS*[^2]

*Staudt, Agustin*[^3]

*Varvasino, Joaquín - CEDLAS*[^4]


## Bienvenidos 

### Sobre este proyecto:

Nos propusimos trasncribir al lenguaje R y Python los apéndices del libro “Pobreza y Desigualdad en América Latina” de Gasparini, Cicowiez y Sosa Escudero que originalmente fueron escritos para Stata y que permitían replicar los datos e información presentados por los autores en el texto. Cada capítulo consta de un apéndice con códigos que permiten llevar a la práctica los conceptos desarrollados. Aquí los traducimos a nuevos lenguajes y los presentamos en un formato amigable para permitir que un público más amplio y de diversas disciplinas pueda aprovecharlos.

El objetivo de este mini-proyecto no es otro que poner a disposición de un público más amplio estas herramientas útiles y mantener actualizado un material único, que ayuda a adentrarse y trabajar sobre la temática de pobreza y desigualdad. Es por eso que este material es de carácter complementario a las explicaciones y detalles conceptuales que se presentan en el libro de texto y los apéndices.


### El libro 

Si esta es la primera vez que te encontrás con este libro, antes de empezar con los códigos, dejanos presentartelo.

El propósito del libro es ayudar al lector interesado en América Latina a que recorra el arduo camino entre los datos y el reporte de resultados rigurosos que puedan contribuir al debate sobre la pobreza y la desigualdad en la región. El volumen busca poner al alcance del lector un conjunto de instrumentos que lo motiven hacia la investigación empírica, y que le permitan producir resultados de la manera más rigurosa posible, para así contribuir a los objetivos últimos de explicar y cambiar la realidad social de la región. Las discusiones conceptuales y analíticas son ilustradas con ejemplos concretos construidos con datos de los países de la región.

```{image} portada_libro.png
:alt: libro
:class: bg-primary mb-1
:width: 60%
:align: center
```

Una enorme ventaja de este trabajo es que se encuentra disponible para todos, ya que se lo puede descargar gratuitamente desde el la [página del libro](https://www.cedlas.econo.unlp.edu.ar/wp/publicaciones/libros/pobreza-y-desigualdad-en-america-latina/). Te invitamos a que puedas recorrerlo, leerlo y dedicarle varios minutos antes de adentrarte en las próximas secciones.

### Cómo aprovechar este material

Un punto importante es que estos códigos que te presentamos están atados a los contenidos y explicaciones que se desarrollan a lo largo de los capítulos del libro. Por eso notarás que los códigos no son autocontenidos al 100%, es decir si bien refuerzan las ideas principales detrás de cada indicador, de cada gráfico o cada estimación, y están acompañados de instrucciones generales, no cubren en profundidad los conceptos teóricos e incluso prácticos detrás de su uso. Por es que decimos que **este material es de carácter complementario a las explicaciones y detalles conceptuales que se presentan en el libro de texto y los apéndices**. Para aprovecharlas al máximo te recomendamos tener abierta junto con la pestaña de R o Python, el pdf del libro de texto para ir siguiendo capitulo a capitulo los contenidos. De esta forma no solo será posible replicar las estimaciones sino también comprenderlas y saber entender qué nos dicen y qué no nos dicen.

### Qué necesitamos antes de arrancar 

Para poder seguir los códigos que te presentamos vas a necesitar descargarte (o al menos tener acceso) a las bases de datos sobre las que iremos trabajando. Estas bases de datos son las encuestas que desarrolla cada país y que el CEDLAS sistematiza para ofrecerlas en un formato usable para los investigadores. En el siguiente [link](https://www.cedlas.econo.unlp.edu.ar/wp/publicaciones/libros/pobreza-y-desigualdad-en-america-latina/#1505501369949-15c93bca-b4f8) encontrarás el repositorio.


<p>&nbsp;</p>

[^1]: __Cristian__ estudió la Licenciatura en Economía (UNNE) y la Maestría en Economía (UNLP). Actualmente colabora como investigador en CEDLAS. Sus intereses se centran en temas de desigualdad, cambio tecnológico y movilidad social. Para entrar en contacto podes escribirle a cristianbonavida@gmail.com. Para conocer más de Cristian, sus proyectos y publicaciones podes visitar su perfil en [twitter](https://twitter.com/crisbonavida) o [linkedin](https://www.linkedin.com/in/cristian-bonavida-966978160/)

[^2]: __Luis__ estudió la Licenciatura en Economía (UNC) y se graduó de la Maestría en Economía (UNLP). Actualmente trabaja como investigador en CEDLAS en temas de desigualdad, mercado laboral y políticas fiscales. Para entrar en contacto podes escribirle a luislaguinge4@gmail.com. Para conocer más de Luis, sus proyectos y publicaciones podes visitar su perfil [twitter](https://twitter.com/luislaguinge) o [linkedin](https://www.linkedin.com/in/luislaguinge/)

[^3]: __Agustín__ estudió la Licenciatura en Economía (UNaM) y la Maestría en Economía (UNLP). Actualmente trabaja como investigador en CAF en temas de cambio climático y en Abrazar en temas de violencia infantil. Para entrar en contacto podes escribirle a agusstaudt@gmail.com. Para conocer más de Joaquín, sus proyectos y publicaciones podes visitar su perfil en su página personal [AS](https://agusstaudt.github.io/profile/)

[^4]: __Joaquín__ estudió la Licenciatura y la Maestría en Economía (UNLP). Actualmente trabaja como investigador en CEDLAS en temas de desigualdad y mercado laboral. Para entrar en contacto podes escribirle a joaquinvarvasino@hotmail.com. Para conocer más de Joaquín, sus proyectos y publicaciones podes visitar su perfil en [twitter](https://twitter.com/mynameisjoaco) o [linkedin](https://www.linkedin.com/in/joaquin-varvasino-826819135/)
