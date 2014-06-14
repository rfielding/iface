#!/usr/bin/python
import os
import sys

class IfParserIn:
    def __init__(self, nm):
        self.name = nm
        self.args = []
        self.ret = None

class IfParserOut:
    def __init__(self, nm):
        self.name = nm
        self.recipient = None
        self.ret = None
        self.args = []

class IfParserMove:
    def __init__(self, nm):
        self.name = nm
        self.fromState = None
        self.toState = None
        self.inAction = None
        self.outAction = None

class IfParserModule:
    def __init__(self, nm):
        self.name = nm
        self.states = {}
        self.ins = {}
        self.outs = {}
        self.moves = []
        self.moduleStart = None
        self.moduleStop = None

class IfParserInteraction:
    def __init__(self, nm):
        self.name = nm
        self.actors = {}
        self.sends = []

class IfParserActor:
    def __init__(self, nm):
        self.name = nm
        self.module = None

class IfParserSend:
    def __init__(self):
        self.sendTo = None
        self.sendMsg = None
        self.sendFrom = None

class IfParser:
    def __init__(self):
        self.token = []
        self.state = "init"
        self.modules = {}
        self.interactions = {}

    def tokenChar(self, c):
        return '0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'z'

    def wsChar(self, c):
        return ' ' == c or '\r' == c or '\n' == c

    def emit(self, t):
        if   t=="@Comment":
            self.state = "comment"
        elif   "@"==t[0]:
            if t=="@Module":
                self.state = "moduleName"
            elif t=="@In":
                self.state = "inName"
            elif t=="@Out":
                self.state = "outName"
            elif t=="@Move":
                self.state = "moveName"
            elif t=="@Interaction":
                self.state = "interactionName"
            elif t=="@Actor":
                self.state = "actorName"
            elif t=="@Send":
                self.state = "sendFrom"
            else:
                raise Exception("unknown keyword %s" % t)
        elif self.state=="wrongToken":
            raise Exception("token in wrong state for %s" % t)
        elif self.state=="comment":
            pass
        elif self.state=="moduleName":
            self.newModule = IfParserModule(t)
            self.modules[t] = self.newModule
            self.state = "moduleStart"
        elif self.state=="moduleStart":
            self.newModule.moduleStart = t
            self.state = "moduleStop"
        elif self.state=="moduleStop":
            self.newModule.moduleStop = t
            self.state = "wrongToken"
        elif self.state=="inName":
            if not t in self.newModule.ins:
                self.newIn = IfParserIn(t)
                self.newModule.ins[t] = self.newIn
            else:
                raise Exception("redefined input %s" % t)
            self.state = "inRet"
        elif self.state=="inRet":
            self.newIn.ret = t
            self.state = "inArg"
        elif self.state=="inArg":
            self.newIn.args.append(t)
        elif self.state=="outName":
            if not t in self.newModule.outs:
                self.newOut = IfParserOut(t)
                self.newModule.outs[t] = self.newOut
            else:
                raise Exception("redefined output %s" % t)
            self.state = "outRet"
        elif self.state=="outRet":
            self.newOut.ret = t
            self.state = "outRecipient"
        elif self.state=="outRecipient":
            self.newOut.recipient = t
            self.state = "outArg"
        elif self.state=="outArg":
            self.newOut.args.append(t)
        elif self.state=="moveName":
            self.move = IfParserMove(t)
            self.newModule.moves.append(self.move)
            self.state = "moveFrom" 
        elif self.state=="moveFrom":
            self.newModule.states[t] = t
            self.move.fromState = t
            self.state = "moveTo"
        elif self.state=="moveTo":
            self.move.toState = t
            self.newModule.states[t] = t
            self.state = "moveType"
        elif self.state=="moveType":
            if t=="In":
                self.state = "moveIn"
            elif t=="Out":
                self.state = "moveOut"
            else:
                raise Exception("unknown move type %s" % t)
        elif self.state=="moveIn":
            self.move.inAction = IfParserIn(t)
            self.state = "moveInArg"
        elif self.state=="moveInArg":
            self.move.inAction.args.append(t)
        elif self.state=="moveOut":
            self.move.outAction = IfParserOut(t)
            self.state = "moveOutArg"
        elif self.state=="moveOutArg":
            self.move.outAction.args.append(t)
        elif self.state=="interactionName":
            self.newInteraction = IfParserInteraction(t)
            self.interactions[t] = self.newInteraction
            self.state = "wrongState"
        elif self.state=="actorName":
            self.newActor = IfParserActor(t)
            self.newInteraction.actors[t] = self.newActor
            self.state = "actorType"
        elif self.state=="actorType":
            self.newActor.module = t
            self.state = "wrongState"
        elif self.state=="sendFrom":
            self.newSend = IfParserSend()
            self.newInteraction.sends.append(self.newSend)
            self.newSend.sendFrom = t
            self.state = "sendMsg"
        elif self.state=="sendMsg":
            self.newSend.sendMsg = t
            self.state = "sendTo"
        elif self.state=="sendTo":
            self.newSend.sendTo = t
            self.state = "wrongState"               
        else:
            raise Exception("unknown state %s for %s" % (self.state,t))
 
    def parsec(self, c):
        if self.wsChar(c):
            if len(self.token) > 0:
                self.emit("".join(self.token))
            self.token = []
        else:
            self.token.append(c)
    
                
    def parse(self, fname):
        with open(fname, "r") as f:
            c = f.read(1)
            while c:
                self.parsec(c)
                c = f.read(1)

    def dotRenderFile(self, f):
        f.write("digraph {\n")
        #List the states
        for mKey in self.modules:
            m = self.modules[mKey]
            for s in m.states:
                if m.moduleStart == s:
                    f.write("    %s_%s [shape=\"doublecircle\" label=\"%s %s\"]\n" % (mKey,s,mKey,s))
                else:
                    f.write("    %s_%s [shape=\"circle\" label=\"%s\"]\n" % (mKey,s,s))
        for mKey in self.modules:
            m = self.modules[mKey]
            for v in m.moves:
                if v.inAction:
                    n = v.inAction.name
                    t = m.ins[n].ret
                    label = "?%s" % (n)
                if v.outAction:
                    n = v.outAction.name
                    t = m.outs[n].recipient
                    label = "%s!%s" % (t,n)
                f.write("    %s_%s -> %s_%s [label=\"%s\\n%s\"]\n" % (mKey,v.fromState, mKey,v.toState,label,v.name))
        f.write("}\n")

    def dotRender(self, fname):
        with open("%s.dot" % fname, "w") as f:
            self.dotRenderFile(f)
        os.system("dot -Tpng -o %s.dot.png %s.dot" % (fname, fname))

    def mscgenRenderFile(self, f, iKey):
        f.write("msc {\n")
        i = self.interactions[iKey]
        #List the actors
        n = 0
        for aKey in i.actors:
            a = i.actors[aKey]
            if n == 0:
                f.write("    ")
            else:
                f.write(",")
            f.write(aKey)
            n = n + 1
        f.write(";\n")
        for s in i.sends:
            f.write("    %s=>%s [label=\"%s\"];\n" % (s.sendFrom, s.sendTo, s.sendMsg))           
        f.write("}\n")

    def mscgenRender(self, fname):
        for iKey in self.interactions:
            with open("%s.msc" % fname, "w") as f:
                self.mscgenRenderFile(f, iKey)
            os.system("mscgen -Tpng -o %s.%s.msc.png %s.msc" % (fname, iKey, fname))

    def interfaceRenderFileModule(self, f, m):
        f.write("public interface %s {\n" % m.name)
        f.write("    /*%s module implements this*/\n" % m.name)
        f.write("    interface In {\n")
        for iKey in m.ins:
            i = m.ins[iKey]
            f.write("        %s %s(" % (i.ret, i.name))
            n = 0
            for a in i.args:
                if n > 0:
                    f.write(",")
                f.write("%s %sArg" % (a,a))
                n = n + 1    
            f.write(");\n")
        f.write("    }\n")
        f.write("    interface Connect {\n")
        f.write("        bool setListener(%s.%s lsn, bool isOn);\n" % (m.name,"Listen.Move"))
        f.write("        bool setListener(%s.%s lsn, bool isOn);\n" % (m.name,"Listen.Send"))
        f.write("        bool setListener(%s.%s lsn, bool isOn);\n" % (m.name,"Listen.Enter"))
        f.write("        bool setListener(%s.%s lsn, bool isOn);\n" % (m.name,"Listen.Exit"))
        f.write("    }\n")
        f.write("    /*%s state machine observers implements this*/\n" % m.name)
        f.write("    interface Listen {\n")
        f.write("        interface Move {\n")
        for mv in m.moves:
            if mv.outAction:
                f.write("            void Move_%s(" % (mv.name))
                f.write("%s snd" % (m.name))
                #nm = mv.outAction.name 
                #f.write("%s %s" % (m.outs[nm].ret,mv.outAction.ret))
                #f.write(",%s %s" % (m.outs[nm].recipient,mv.outAction.recipient))
                #n = 0
                #for a in mv.outAction.args:
                #    f.write(",%s %s" % (m.outs[nm].args[n],a))
                #    n = n + 1
                f.write(");\n")
        f.write("        }\n")
        f.write("        interface Send {\n")
        for oKey in m.outs:
            o = m.outs[oKey]
            f.write("            void Send_%s(" % (o.name))
            f.write("%s snd" % (m.name))
            f.write(",%s rcv" % (o.recipient))
            n = 0
            for a in o.args:
                f.write(",%s %sArg" % (a,a))
                n = n + 1
            f.write(");\n")
        f.write("        }\n")
        f.write("        interface Enter {\n")
        for s in m.states:
            f.write("            void Enter_%s(%s snd);\n" % (s,m.name))
        f.write("        }\n")
        f.write("        interface Exit {\n")
        for s in m.states:
            f.write("            void Exit_%s(%s snd);\n" % (s,m.name))
        f.write("        }\n")
        f.write("    }\n")
        f.write("}\n")

    def interfaceRenderFile(self, f):
        for mKey in self.modules:
            m = self.modules[mKey]
            self.interfaceRenderFileModule(f, m)        

    def interfaceRender(self, fname):
        with open("%s.java" % fname, "w") as f:
            self.interfaceRenderFile(f)

p = IfParser()
fname = "example.if"
p.parse(fname)
p.dotRender(fname)
p.mscgenRender(fname)
p.interfaceRender(fname)        