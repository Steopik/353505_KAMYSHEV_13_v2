FROM openjdk:17

WORKDIR /app

COPY app.jar .
COPY lib/mysql-connector-j-9.2.0.jar lib/mysql-connector-j-9.2.0.jar

ENTRYPOINT ["java", "-jar", "app.jar"]