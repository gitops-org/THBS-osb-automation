package com.ragsInfo.controller;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import javax.faces.bean.SessionScoped;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.faces.event.ActionEvent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ragsInfo.entity.Role;
import com.ragsInfo.service.UserWizardService;

@ManagedBean
@RequestScoped
@Component
public class RoleController implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private Role role=new Role();
	private List<Role> rolesList = new ArrayList<>();
	private boolean editflag;
	
	
	@Autowired
	private UserWizardService userWizardService;
	FacesMessage msg=null;
	
	
	

	public boolean isEditflag() {
		return editflag;
	}

	public void setEditflag(boolean editflag) {
		this.editflag = editflag;
	}

	public List<Role> getRolesList() {
		return rolesList;
	}

	public void setRolesList(List<Role> rolesList) {
		this.rolesList = rolesList;
	}

	public Role getRole() {
		return role;
	}

	public void setRole(Role role) {
		this.role = role;
	}

	public UserWizardService getUserWizardService() {
		return userWizardService;
	}

	public void setUserWizardService(UserWizardService userWizardService) {
		this.userWizardService = userWizardService;
	}
	
	@PostConstruct
	public void init() {
		try {
			setEditflag(false);
		rolesList.clear();
			rolesList = userWizardService.getRoleList();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	
	
	/**
	 * 
	 */
	public void saveRole() {
		try {
			userWizardService.saveRole(role);
			init();
			msg = new FacesMessage("Successful Created", "Role :" + role.getRoleName());
			FacesContext.getCurrentInstance().addMessage(null, msg);

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	
	
	 /**
		 * @param load the roles
		 */
		public void loadRole(ActionEvent e) {
			try {
				init();	
				setEditflag(false);
				ExternalContext ec = FacesContext.getCurrentInstance()
	                    .getExternalContext();
							ec.redirect(ec.getRequestContextPath()
							        + "/pages/role.xhtml");
						} catch (IOException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
		}
		
		
		
		
		/**
		 * @param user
		 */
		public void deleteRole(Role role) {
		    System.out.println(role);
		    try {
				userWizardService.deleteRole(role);
				init();
				msg = new FacesMessage(FacesMessage.SEVERITY_INFO, "Deletion was Successful", "Deleted role is :" + role.getRoleName());
				FacesContext.getCurrentInstance().addMessage(null, msg);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		
		
		/**
		 * @param user
		 */
		public void editRole(Role role) {
		    System.out.println(role);
		    try {
		    	setRole(role);
		    	setEditflag(true);
		    	ExternalContext ec = FacesContext.getCurrentInstance()
	                    .getExternalContext();
							ec.redirect(ec.getRequestContextPath()
							        + "/pages/role.xhtml");
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		
		
		/**
		 * 
		 */
		public void addRole() {
		    try {
		    	Role role=new Role();
		    	setRole(role);
		    	setEditflag(false);
		    	ExternalContext ec = FacesContext.getCurrentInstance()
	                    .getExternalContext();
							ec.redirect(ec.getRequestContextPath()
							        + "/pages/role.xhtml");
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}


		

}