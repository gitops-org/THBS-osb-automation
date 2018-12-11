package com.journaldev.prime.faces.beans;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.ViewScoped;
import javax.faces.context.FacesContext;

import org.primefaces.event.FlowEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.journaldev.hibernate.entity.User;
import com.journaldev.spring.service.UserWizardService;

@ManagedBean
@ViewScoped
@Component
public class UserWizardController implements Serializable {

	private User user = new User();
	private List<User> usersList = new ArrayList<>();

	public List<User> getUsersList() {
		return usersList;
	}

	public void setUsersList(List<User> usersList) {
		this.usersList = usersList;
	}

	@Autowired
	private UserWizardService userWizardService;

	@PostConstruct
	public void init() {
		try {
			usersList.clear();
			usersList = userWizardService.getUsersList();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public UserWizardService getUserWizardService() {
		return userWizardService;
	}

	public void setUserWizardService(UserWizardService userWizardService) {
		this.userWizardService = userWizardService;
	}

	private boolean skip;

	public User getUser() {
		return user;
	}

	public void setUser(User user) {
		this.user = user;
	}

	public boolean isSkip() {
		return skip;
	}

	public void setSkip(boolean skip) {
		this.skip = skip;
	}

	public String onFlowProcess(FlowEvent event) {
		if (skip) {
			skip = false; // reset in case user goes back
			return "confirm";
		} else {
			return event.getNewStep();
		}	
	}

	/**
	 * save the user details
	 */
	public void save() {
		try {
			userWizardService.register(user);
			System.out.println("User is saved to database");
			init();
		/*	FacesMessage msg = new FacesMessage("Successful", "Welcome :" + user.getFirstname());
			FacesContext.getCurrentInstance().addMessage(null, msg);*/

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}