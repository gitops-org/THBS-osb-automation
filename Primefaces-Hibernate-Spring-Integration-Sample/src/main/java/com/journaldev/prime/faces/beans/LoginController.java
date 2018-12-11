package com.journaldev.prime.faces.beans;
import java.io.IOException;

import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;

import org.springframework.stereotype.Component;

import com.journaldev.hibernate.entity.Login;

@ManagedBean
@SessionScoped
@Component
public class LoginController {
     
	private Login login =new Login();

   
    public Login getLogin() {
		return login;
	}

	public void setLogin(Login login) {
		this.login = login;
	}




	public void login() {
        FacesMessage message = null;
        boolean loggedIn = false;
        try { 
        if(login.getUsername() != null && login.getUsername().equals("admin") && login.getPassword() != null && login.getPassword().equals("admin")) {
            loggedIn = true;
            message = new FacesMessage(FacesMessage.SEVERITY_INFO, "Welcome", login.getUsername());
            ExternalContext ec = FacesContext.getCurrentInstance()
                    .getExternalContext();
					ec.redirect(ec.getRequestContextPath()
					        + "/home.xhtml");
				
        } else {
            loggedIn = false;
            message = new FacesMessage(FacesMessage.SEVERITY_WARN, "Loggin Error", "Invalid credentials");
        }
         
        FacesContext.getCurrentInstance().addMessage(null, message);
        } catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }   
}