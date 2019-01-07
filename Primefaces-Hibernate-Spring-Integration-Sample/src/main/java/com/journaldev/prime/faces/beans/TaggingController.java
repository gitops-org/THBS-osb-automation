package com.journaldev.prime.faces.beans;

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

import com.journaldev.hibernate.entity.Tagging;
import com.journaldev.hibernate.entity.User;
import com.journaldev.spring.service.UserWizardService;

@ManagedBean
@RequestScoped
@Component
public class TaggingController implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private Tagging tag = new Tagging();
	private List<Tagging> taggingsList = new ArrayList<>();
	private boolean editflag;
	
	private List<Tagging> selectedTagsList = new ArrayList<>();
	private boolean multiSelectedTag;
	private Tagging selectedTag;
	
	
	

	public Tagging getSelectedTag() {
		return selectedTag;
	}

	public void setSelectedTag(Tagging selectedTag) {
		this.selectedTag = selectedTag;
	}


	@Autowired
	private UserWizardService userWizardService;
	
	FacesMessage msg = null;

	@Autowired
	private UserWizardController userWizardController;
	

	public UserWizardController getUserWizardController() {
		return userWizardController;
	}

	public void setUserWizardController(UserWizardController userWizardController) {
		this.userWizardController = userWizardController;
	}

	public boolean isEditflag() {
		return editflag;
	}

	public void setEditflag(boolean editflag) {
		this.editflag = editflag;
	}

	public List<Tagging> getTaggingsList() {
		return taggingsList;
	}

	public void setTaggingsList(List<Tagging> taggingsList) {
		this.taggingsList = taggingsList;
	}

	public Tagging getTag() {
		return tag;
	}

	public void setTag(Tagging tag) {
		this.tag = tag;
	}

	public UserWizardService getUserWizardService() {
		return userWizardService;
	}

	public void setUserWizardService(UserWizardService userWizardService) {
		this.userWizardService = userWizardService;
	}

	
	public List<Tagging> getSelectedTagsList() {
		return selectedTagsList;
	}

	public void setSelectedTagsList(List<Tagging> selectedTagsList) {
		this.selectedTagsList = selectedTagsList;
	}
	
	
	

	public boolean isMultiSelectedTag() {
		return multiSelectedTag;
	}

	public void setMultiSelectedTag(boolean multiSelectedTag) {
		this.multiSelectedTag = multiSelectedTag;
	}

	@PostConstruct
	public void init() {
		try {
			setEditflag(false);
			taggingsList.clear();
			selectedTagsList.clear();
			taggingsList = userWizardService.getTaggingList();
			userWizardController.getSelectedUsersList().clear();
			tag.setSelectedTag(false);
			setMultiSelectedTag(false);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	/**
	 * 
	 */
	public void saveTagging() {
		try {
			userWizardService.saveTagging(tag);
			init();
			msg = new FacesMessage("Successful Created", "Tagging :" + tag.getTagName());
			FacesContext.getCurrentInstance().addMessage(null, msg);

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	/**
	 * @param load
	 *            the Taggings
	 */
	public void loadTagging(ActionEvent e) {
		try {
			init();
			setEditflag(false);
			ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
			ec.redirect(ec.getRequestContextPath() + "/pages/tagging.xhtml");
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}

	/**
	 * @param user
	 */
	public void deleteTagging(Tagging tag) {
		System.out.println(tag);
		try {
			userWizardService.deleteTagging(tag);
			init();
			msg = new FacesMessage(FacesMessage.SEVERITY_INFO, "Deletion was Successful",
					"Deleted Tagging is :" + tag.getTagName());
			FacesContext.getCurrentInstance().addMessage(null, msg);
			ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
			ec.redirect(ec.getRequestContextPath() + "/pages/tagging.xhtml");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	/**
	 * @param user
	 */
	public void editTagging(Tagging tag) {
		System.out.println(tag);
		try {
			setTag(tag);
			setEditflag(true);
			ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
			ec.redirect(ec.getRequestContextPath() + "/pages/tagging.xhtml");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	/**
	 * 
	 */
	public void addTagging() {
		try {
			Tagging tag = new Tagging();
			setTag(tag);
			setEditflag(false);
			ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
			ec.redirect(ec.getRequestContextPath() + "/pages/tagging.xhtml");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void selectedList(Tagging tagging) {
		
		List<Tagging> taggingsList2 = getTaggingsList();
		
		if(taggingsList2.contains(tagging))
		{
			if(!tagging.isSelectedTag())
			{
				for (Tagging tagging2 : taggingsList2) {
					tagging2.setSelectedTag(false);
				}
				selectedTag=tagging;
			}else
			{
				selectedTag=null;
			}
		}
	}

	
	/**
	 * Associate Customers
	 */
	public void associateCustomers()
	{
		try {
			List<User> selectedUsersList = userWizardController.getSelectedUsersList();
			if (selectedUsersList.isEmpty()) {
				msg = new FacesMessage(FacesMessage.SEVERITY_ERROR, "No  User is selected",
						"No Association is possible :" + getSelectedTag().getTagName());
				FacesContext.getCurrentInstance().addMessage(null, msg);
			} else if (getSelectedTag() == null) {
				msg = new FacesMessage(FacesMessage.SEVERITY_ERROR, "No  Tag is selected",
						"No Association is possible atleast select one tag :");
				FacesContext.getCurrentInstance().addMessage(null, msg);
			} else {
				for (User user : selectedUsersList) {
					user.setTagging(getSelectedTag());
					userWizardService.register(user);
				}
				msg = new FacesMessage(FacesMessage.SEVERITY_INFO, "Users Tagging",
						" Users Association is Succesful :" + getSelectedTag().getTagName());
				FacesContext.getCurrentInstance().addMessage(null, msg);
			}
			selectedTagsList.clear();
			ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
			ec.redirect(ec.getRequestContextPath() + "/pages/tagging.xhtml");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
}