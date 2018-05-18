package com.iss.model;

public class UserBean {

	private int id;
	private String name;
	private String profession;
	private double remuneration;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getProfession() {
		return profession;
	}
	public void setProfession(String profession) {
		this.profession = profession;
	}
	public double getRemuneration() {
		return remuneration;
	}
	public void setRemuneration(double remuneration) {
		this.remuneration = remuneration;
	}
	/**
	 * @param id
	 * @param name
	 * @param profession
	 * @param remuneration
	 */
	public UserBean(int id, String name, String profession, double remuneration) {
		super();
		this.id = id;
		this.name = name;
		this.profession = profession;
		this.remuneration = remuneration;
	}
	
	
}
