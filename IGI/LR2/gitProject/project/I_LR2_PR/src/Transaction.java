import java.time.LocalDateTime;



public class Transaction {
    public int IdTransactions;
    public LocalDateTime DataTimeOfTransaction = null;
    public double Sum;
    public TypeOfTransaction TypeOfTransaction;
    public String Description = null;

    public Transaction(TypeOfTransaction typeOfTransaction, double sum){
        TypeOfTransaction = typeOfTransaction;
        Sum = sum;
    }

    public Transaction(TypeOfTransaction typeOfTransaction, double sum
    , LocalDateTime dateTimeOfTeansiction){
        this(typeOfTransaction, sum);
        DataTimeOfTransaction = dateTimeOfTeansiction;
    }
    
    public Transaction(TypeOfTransaction typeOfTransaction, double sum
    ,String description){
        this(typeOfTransaction, sum);
        Description = description;
    }

    public Transaction(TypeOfTransaction typeOfTransaction, double sum
    , LocalDateTime dateTimeOfTeansiction, String description){
        this(typeOfTransaction, sum, dateTimeOfTeansiction);
        Description = description;
    }

    public Transaction(int id, TypeOfTransaction typeOfTransaction, double sum
    , LocalDateTime dateTimeOfTeansiction, String description){
        this(typeOfTransaction, sum, dateTimeOfTeansiction, description);
        IdTransactions = id;
    }

    
}
