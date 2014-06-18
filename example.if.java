
public class PreconditionException extends RuntimeException {
    public PreconditionException(String msg) {
        super(msg);
    }
}

/* Get a cooperating set of APIs */
public interface ApiSet {
    Api[] getApis();
}

public interface Api {
    void addListener(Api.Listener lsn);

    /* Untyped msging API*/
    Object doRcv(String msg, Object[] args);
    boolean doRcv_Precondition(String msg, Object[] args);
    Object doSend(Api a, String msg, Object[] args);
    String[] messageNames();
    String[] messageArgTypes(String msg);
    String messageArgReturnType(String msg);

    interface Listener {
        void enter(String name);
        void send(String name, String exiting, String entering,
                       Api target, String msg, Object[] args
        );
        void sendReturned(String name, String exiting, String entering,
                               Api target, String msg, Object[] args, Object ret
        );
        void rcv(String name, String exiting, String entering,
                      String msg, Object[] args
        );
        void rcvReturn(String name, String exiting, String entering,
                            String msg, Object[] args,Object arg
        );
        void exit(String name);
    }
}

/* Typed send API*/
public interface ApiG extends Api {
    N doNotify(Z ZArg) throws PreconditionException;
    boolean Precondition_doNotify(Z ZArg);
}

/* Typed send API*/
public interface ApiA extends Api {
    void setZ(ApiB ApiBArg) throws PreconditionException;
    F doSomeF(X XArg) throws PreconditionException;
    G doSomeG(Y YArg) throws PreconditionException;
    void setB(ApiB ApiBArg) throws PreconditionException;
    boolean Precondition_setZ(ApiB ApiBArg);
    boolean Precondition_doSomeF(X XArg);
    boolean Precondition_doSomeG(Y YArg);
    boolean Precondition_setB(ApiB ApiBArg);
}

/* Typed send API*/
public interface ApiB extends Api {
    K doSomeK(X XArg) throws PreconditionException;
    boolean Precondition_doSomeK(X XArg);
}

/* Typed send API*/
public interface ApiC extends Api {
}
