package com.javacodegeeks.example.util;

public class PersonModel {
	String firstName, lastName, school;
	int rollNumber;
	public String getFirstName() {
		return firstName;
	}
	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}
	public String getLastName() {
		return lastName;
	}
	public void setLastName(String lastName) {
		this.lastName = lastName;
	}
	public String getSchool() {
		return school;
	}
	public void setSchool(String school) {
		this.school = school;
	}
	public int getRollNumber() {
		return rollNumber;
	}
	public void setRollNumber(int rollNumber) {
		this.rollNumber = rollNumber;
	}
	
	@Override
	public String toString(){
		return "Hello, "+firstName+" "+lastName+"! Welcome to "+school+ "!";
	}
}
