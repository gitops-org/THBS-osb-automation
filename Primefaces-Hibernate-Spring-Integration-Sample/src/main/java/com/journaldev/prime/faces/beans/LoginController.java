package com.journaldev.prime.faces.beans;
import java.io.IOException;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.journaldev.hibernate.entity.Login;
import com.journaldev.hibernate.entity.User;

@ManagedBean
@SessionScoped
@Component
public class LoginController{
	
	private Login login;
    private String thbsVersion="1.0";
    private Date buildDate=new Date();
    HashMap<String, User> userHashMap = new HashMap<>();
    @Autowired
    private UserWizardController userWizardController;
    
    
    public UserWizardController getUserWizardController() {
		return userWizardController;
	}

	public void setUserWizardController(UserWizardController userWizardController) {
		this.userWizardController = userWizardController;
	}

	public String getThbsVersion() {
		return thbsVersion;
	}

	public void setThbsVersion(String thbsVersion) {
		this.thbsVersion = thbsVersion;
	}

	public Date getBuildDate() {
		return buildDate;
	}

	public void setBuildDate(Date buildDate) {
		this.buildDate = buildDate;
	}

	public Login getLogin() {
		return login;
	}

	public void setLogin(Login login) {
		this.login = login;
	}


	@PostConstruct
	public void init() {
		  login =new Login();
		// get uer Information
		  
	}

	HttpSession session=null;


	public void login() throws Exception {
        FacesMessage message = null;
        boolean loggedIn = false;
		try {
			userHashMap.clear();
			List<User> usersList = userWizardController.getUsersList();
			for (User user : usersList) {
				userHashMap.put(user.getUsername(), user);
			}
			if (login.getUsername() != null && !userHashMap.isEmpty() && userHashMap.containsKey(login.getUsername().toLowerCase())) {

				String password = userHashMap.get(login.getUsername().toLowerCase()).getPassword();
				if (login.getPassword() != null && login.getPassword().equals(password)) {
					loggedIn = true;
				} else {
					loggedIn = false;
					message = new FacesMessage(FacesMessage.SEVERITY_WARN, "Loggin Error", "Invalid password");
				}
			} else {
				loggedIn = false;
				message = new FacesMessage(FacesMessage.SEVERITY_WARN, "Loggin Error", "Invalid UserName");

			}

			if (loggedIn) {
				message = new FacesMessage(FacesMessage.SEVERITY_INFO, "Welcome", login.getUsername());

				HttpServletRequest request = (HttpServletRequest) FacesContext.getCurrentInstance().getExternalContext()
						.getRequest();
				session = request.getSession();
				session.setMaxInactiveInterval(10 * 60);
				session.setAttribute("user", login.getUsername());
				session.setAttribute("password", login.getPassword());

				ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
				ec.redirect(ec.getRequestContextPath() + "/pages/home.xhtml");
				userWizardController.init();
			}/* else {
				//loggedIn = false;
				message = new FacesMessage(FacesMessage.SEVERITY_WARN, "Loggin Error", "Invalid credentials");
			}
*/
			FacesContext.getCurrentInstance().addMessage(null, message);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    } 
	
	
	
	public void changePassword() {
		try {
			User user = userHashMap.get(login.getUsername());
			getUserWizardController().setUser(user);
			ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
			ec.redirect(ec.getRequestContextPath() + "/pages/changePassword.xhtml");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	
	public String logout() {
        FacesContext.getCurrentInstance().getExternalContext().invalidateSession();
        return "/pages/login.xhtml?faces-redirect=true";
    }
	
}