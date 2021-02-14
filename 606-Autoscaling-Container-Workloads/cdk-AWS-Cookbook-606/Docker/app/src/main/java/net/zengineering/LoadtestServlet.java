package net.zengineering.java.loadtest;

import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.Locale;
import java.util.TimeZone;

import javax.servlet.ServletException;
import javax.servlet.ServletInputStream;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.net.InetAddress;
import java.net.UnknownHostException;

public class LoadtestServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
	private DateFormat httpDateFormat = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z", Locale.US);
	
	public LoadtestServlet() {
		httpDateFormat.setTimeZone(TimeZone.getTimeZone("GMT"));
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		long now = System.currentTimeMillis();
		String timeStr = request.getParameter("time");
		String httpStatusStr = request.getParameter("http-status");
		int httpStatus = (httpStatusStr!=null?Integer.parseInt(httpStatusStr):200);
		long maxTime = (timeStr != null ? Long.parseLong(timeStr) : 0L);

		long time = maxTime;

		if (request.getRequestURI().endsWith("/cpu")) {
		
			double value = 9.9;
			while (System.currentTimeMillis() <= (now + 99999999)) {
				value = value / 1.0000001;
				value = value * 1.00000015;
				if (value > Double.MAX_VALUE / 2) {
					value = 1.0;
				}
			}
			finishTest(request, response, (System.currentTimeMillis() - now), httpStatus, "success", "value=" + value);

		} else if (request.getRequestURI().endsWith("/healthcheck")) {
			// aws load balancer health check

			double value = 9.9;
			while (System.currentTimeMillis() <= (now + 3000)) {
				value = value / 1.0000001;
				value = value * 1.00000015;
				if (value > Double.MAX_VALUE / 2) {
					value = 1.0;
				}
			}
			finishTest(request, response, (System.currentTimeMillis() - now), httpStatus, "success", "value=" + value);

		} else {
			finishTest(request, response, (System.currentTimeMillis() - now), 400, "error", 
					"");
		}

	}

	private void finishTest(HttpServletRequest request, HttpServletResponse response, long timeElapsed, int statusCode, String result, String info) {
		try {
			response.setContentType("application/json");
			response.setStatus(statusCode);
			ServletOutputStream responseOS = response.getOutputStream();
			InetAddress ip;
			ip = InetAddress.getLocalHost();
			String hostname = ip.getHostName();
			String body = "{\n   \"URL\":\"" + request.getRequestURL() + "\",\n   \"ContainerLocalAddress\":\"" + request.getLocalAddr() + ":" + request.getLocalPort() + "\",\n   \"ProcessingTimeTotalMilliseconds\":\"" + timeElapsed + "\",\n   \"LoadBalancerPrivateIP\":\"" + request.getRemoteHost() + "\",\n   \"ContainerHostname\":\"" + hostname + "\",\n   \"CurrentTime\":\"" + System.currentTimeMillis() + "\"\n}";
			responseOS.print(body);
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
}
