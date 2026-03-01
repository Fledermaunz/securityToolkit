package portscanner;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class portscanner {
    ArrayList<Integer> ports = new ArrayList<>();
    ArrayList<Integer> openPorts = new ArrayList<>();
    private int timeout;
    private String target;
    private int threadPoolSize;


    public String getTarget() {
        return target;
    }

    public void setTarget(String target) {
        this.target = target;
    }

    portscanner(String target, int timeout, int threadPoolSize) {
        this.target = target;
        this.timeout = timeout;
        this.threadPoolSize = threadPoolSize;
    }

}

