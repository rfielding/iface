public interface Api {
    void addListener(Api.Listener lsn);
    interface Listener {
        void stateEnter(String name);
        void stateSend(String name, String exiting, String entering, Api target, String msg, Object[] args);
        void stateSendReturned(String name, String exiting, String entering, Api target, String msg, Object[] args, Object ret);
        void stateRcv(String name, String exiting, String entering, String msg, Object[] args);
        void stateRcvReturn(String name, String exiting, String entering, String msg, Object[] args,Object arg);
        void stateExit(String name);
    }
}
public interface ApiG extends Api {
    N doNotify(Z ZArg);
    boolean Precondition_doNotify(Z ZArg);
}
public interface ApiA extends Api {
    void setZ(ApiB ApiBArg);
    F doSomeF(X XArg);
    G doSomeG(Y YArg);
    void setB(ApiB ApiBArg);
    boolean Precondition_setZ(ApiB ApiBArg);
    boolean Precondition_doSomeF(X XArg);
    boolean Precondition_doSomeG(Y YArg);
    boolean Precondition_setB(ApiB ApiBArg);
}
public interface ApiB extends Api {
    K doSomeK(X XArg);
    boolean Precondition_doSomeK(X XArg);
}
public interface ApiC extends Api {
}
