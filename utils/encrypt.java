import utils.*;

public class encrypt {
  public static void main (String[] args) {
    String dbPass;
    if (args.length != 2) {
      System.out.println("Bad number of Arguments. SYNTAX: java encrypt User Password");
      System.exit(1);
    }
    AltEncrypter cypher = new AltEncrypter("cypherkey" + args[0]);
    dbPass = cypher.encrypt(args[1]);
    System.out.println(dbPass);
  }
}
