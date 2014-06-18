
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
