package portscanner;

import java.lang.reflect.Array;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.List;

public class portscanner {
    private List<Integer> ports;
    private List<Integer> openPorts;
    private int timeout;
    private String target;
    private int threadPoolSize;


    public portscanner(String target, int timeout, int threadPoolSize) {
        this.target = target;

        if (ports == null) {
            this.ports = new ArrayList<>();
            for (int i = 1; i <= 1024; i++) {
                this.ports.add(i);  
            }
        } else {
            this.ports = ports;
        }

        this.timeout = timeout;
        this.threadPoolSize = threadPoolSize;

        this.openPorts = threadPoolSize;
    }

    public PortScanner(String target, List<Integer> ports) {
        this(target, ports, 1000, 10);  
    }

    public PortScanner(String target) {
        this(target, null, 1000, 10);       
    }

    
}


package portscanner;

public class portScannerWithResolution extends portscanner {
    
}
