package com.ragsInfo.filter;
import java.io.IOException;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;


public class AuthorizationFilter implements Filter {

	public AuthorizationFilter() {
	}

	@Override
	public void init(FilterConfig filterConfig) throws ServletException {

	}

	@Override
	public void doFilter(ServletRequest request, ServletResponse response,
			FilterChain chain) throws IOException, ServletException {
		try {

			HttpServletRequest reqt = (HttpServletRequest) request;
	        HttpServletResponse resp = (HttpServletResponse) response;
	        HttpSession session = reqt.getSession(false);
			String reqURI = reqt.getRequestURI();
			
			if (reqURI.indexOf("/login.xhtml") >= 0
					|| (session != null && session.getAttribute("user") != null))
				
			{	
				chain.doFilter(request, response);
			}else
			{
					resp.sendRedirect(reqt.getContextPath() + "/faces/pages/login.xhtml");	
		}
		}catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}

	@Override
	public void destroy() {

	}
}
