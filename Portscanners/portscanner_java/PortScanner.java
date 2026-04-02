import java.net.Socket;
import java.net.InetSocketAddress;
import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class PortScanner {
    
    public static void scanPort(String host, int port, int timeout) {
        try (Socket socket = new Socket()) {
            socket.connect(new InetSocketAddress(host, port), timeout);
            System.out.println("Port " + port + " is OPEN");
        } catch (IOException ignored) {
        }
    }

    public static void main(String[] args) {
        String host = "127.0.0.1";
        int timeout = 200;

        int threads = 100;
        ExecutorService executor = Executors.newFixedThreadPool(threads);

        for (int port = 1; port <= 65535; port++) {
            final int currentPort = port;
            executor.submit(() -> scanPort(host, currentPort, timeout));
        }
        executor.shutdown();
    }

}