public class Configs {
    protected String dbHost = "db";
    protected String dbPort = "3306";
    protected String dbUser = System.getenv("MYSQL_USER");
    protected String dbPass = System.getenv("MYSQL_PASSWORD");
    protected String dbName = System.getenv("MYSQL_DATABASE");
}
