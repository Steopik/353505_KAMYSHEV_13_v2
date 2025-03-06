import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Scanner;

public class App {
    public static void main(String[] args) throws Exception {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("Input command");
            String operation = scanner.nextLine();
        
            switch (operation) {
                case "/q":
                    scanner.close();
                    return;
            
                case "/r":
                    read();
                    break;

                case "/w":
                    write();
                    break;
                default:
                    break;
            }

        }
    }

    private static void write(){
        try{
            System.out.println("Inserting in DB");
            Scanner scanner = new Scanner(System.in);
            System.out.println("Income/Expenditure?");
            String ans = scanner.nextLine();
            TypeOfTransaction typeOfTransaction = (ans.equals("Income")?
            TypeOfTransaction.Income: TypeOfTransaction.Expenditure);

            System.out.println("Sum");
            double sum = scanner.nextDouble();
            scanner.nextLine();

            System.out.println("Data");
            ans = scanner.nextLine();
            LocalDateTime dateTime = LocalDateTime.parse(ans, DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm"));

            System.out.println("Description");
            String description = scanner.nextLine();
            Transaction transaction = new Transaction(typeOfTransaction, sum
            , dateTime
            , description);
            
            DataBaseHandler dataBaseHandler = new DataBaseHandler();

            dataBaseHandler.writeNewTransiction(transaction);
            System.out.println("Insert in DB");
        }catch (Exception e){
            System.out.println(e.toString());
        }
    }

    private static void read(){
        DataBaseHandler dataBaseHandler = new DataBaseHandler();
        List<Transaction> trList = dataBaseHandler.readAllTransactions();
        System.out.println("Information from db is displayed");
        if (trList.size() == 0) {
            System.out.println("db is empty");
            return;
        }
        for (int i = 0; i < trList.size(); i++){
            Transaction transaction = trList.get(i);
            String line = DateTimeFormatter.ofPattern("dd.MM.yy HH:mm").format(transaction.DataTimeOfTransaction) 
            + "\t\t|" + (transaction.TypeOfTransaction == TypeOfTransaction.Income? "Income     ": "Expenditure") 
            + "\t\t|"  + transaction.Sum + "\t\t|" + transaction.Description;
            
            System.out.println(line);
        }
        System.out.println("The information is out");
    }
}
