import java.net.*;
import org.apache.xmlrpc.client.*;

public class SendSMS {

	private static String host = "172.29.198.18";
	private static String to = "2612";
	private static String callback = "3000";
	private static String display = "Hello World!";

	public static void main (String [] args) {
		try {
			int i;
			XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
			config.setServerURL(new URL("http://" + host + "/RPC2"));
			XmlRpcClient client = new XmlRpcClient();
			client.setConfig(config);

			Object[] params = new Object[]{new String("GW-DECT/admin"), new String("ip6000")};
			Integer session = (Integer) client.execute("session_login", params);

			params = new Object[]{session, 0};
			for(i = 0; i < 1000; i++)
				client.execute("session_receive", params);

			params = new Object[]{session};
			client.execute("session_logout", params);

		} catch (Exception exception) {
			System.err.println("SendSMS: " + exception);
		}
	}
}

