import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.sql.ResultSet;

public class DataBaseHandler extends Configs{
    Connection dbConnection;

    public Connection getdbConnection() 
    throws ClassCastException, SQLException{
        try{
            String conneString = "jdbc:mysql://" + dbHost + ":" + dbPort + "/" + dbName;
            dbConnection = DriverManager.getConnection(conneString
            , dbUser, dbPass);
            
            
        }catch (Exception e){
            System.out.println(e.toString());
        }
        return dbConnection;
    }

    public void writeNewTransiction(Transaction transaction){
        String insert = "Insert INTO " + DBConst.Transaction_TABLE + "(" +
        DBConst.Transaction_SUM + "," + DBConst.Transaction_DESCRIPTION + "," + 
        DBConst.Transaction_DATETIME + "," + DBConst.Transaction_TYPE + ")" +
        "VALUES(?,?,?,?)";

        try{
            PreparedStatement prSt = getdbConnection().prepareStatement(insert);
            prSt.setString(1, String.valueOf(transaction.Sum));
            prSt.setString(2, transaction.Description);
            prSt.setString(3, DateTimeFormatter.ofPattern("dd.MM.yy HH:mm").format(transaction.DataTimeOfTransaction));
            prSt.setString(4, String.valueOf(transaction.TypeOfTransaction == TypeOfTransaction.Income? 1: 0));
            prSt.executeUpdate();
        }catch (SQLException e){
            System.out.println("An exeption occurred when writing data to the database: " + e.toString());
        }
        
    }

    public ResultSet readTransiction(Transaction transaction){
        ResultSet resSet = null;
        String select = "SELECT * FROM " + DBConst.Transaction_TABLE + " WHERE " +
            DBConst.Transaction_ID + "=?";
            try{
                PreparedStatement prSt = getdbConnection().prepareStatement(select);
                prSt.setString(1, String.valueOf(transaction.IdTransactions));
                resSet = prSt.executeQuery();
            }catch (SQLException e){
                System.out.println("An exeption occurred when receiving data from the database: " + e.toString());
            }
        

        return resSet;
    }

    public List<Transaction> readAllTransactions() {
        ResultSet resSet = null;
        List<Transaction> transactions = new ArrayList<>();
        String select = "SELECT * FROM " + DBConst.Transaction_TABLE; 
        try {
            PreparedStatement prSt = getdbConnection().prepareStatement(select);
            resSet = prSt.executeQuery();

            while (resSet.next()) {
                int id = resSet.getInt(DBConst.Transaction_ID); 
                double sum = resSet.getDouble(DBConst.Transaction_SUM);
                String description = resSet.getString(DBConst.Transaction_DESCRIPTION);
                String dateTimeString = resSet.getString(DBConst.Transaction_DATETIME);
                int typeInt = resSet.getInt(DBConst.Transaction_TYPE);

                LocalDateTime dataTimeOfTransaction = LocalDateTime.parse(dateTimeString, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
                TypeOfTransaction typeOfTransaction = (typeInt == 1) ? TypeOfTransaction.Income : TypeOfTransaction.Expenditure;

                Transaction transaction = new Transaction(id, typeOfTransaction, sum, dataTimeOfTransaction, description); 

                transactions.add(transaction);
            }


        } catch (SQLException e) {
            System.out.println("An exeption occurred when receiving data from the database: " + e.toString());
        } catch (Exception e){
            System.out.println("An exeption occurred when receiving data from the database: " + e.toString());
        }

        
        return transactions;
    }
    
}
