import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ClientProfile.css";

const ClientProfile = () => {
    const navigate = useNavigate();
    const [clientData, setClientData] = useState(null);
    const [plans, setPlans] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const token = localStorage.getItem("token");
        let client_id = localStorage.getItem("client_id");

        console.log("LocalStorage Token:", token);  // Debugging
        console.log("LocalStorage Client ID:", client_id);

        if (!token) {
            alert("You must be logged in to view your profile.");
            navigate("/login");
            return;
        }

        if (!client_id) {
            fetch(`http://localhost:8000/api/userinfo`, {
                method: "GET",
                headers: { "Authorization": `Bearer ${token}` },
            })
            .then(response => response.json())
            .then(data => {
                if (data.client_id) {
                    localStorage.setItem("client_id", data.client_id);
                    client_id = data.client_id;
                    fetchClientData(client_id, token);
                    fetchPlans(client_id, token);
                } else {
                    alert("Failed to retrieve client information.");
                    navigate("/login");
                }
            })
            .catch(error => console.error("Error fetching client_id:", error));
        } else {
            fetchClientData(client_id, token);
            fetchPlans(client_id, token);
        }

    }, [navigate]);

    const fetchClientData = async (client_id, token) => {
        try {
            console.log("Fetching client data...");
            const response = await fetch(`http://localhost:8000/api/client/${client_id}`, {
                method: "GET",
                headers: { "Authorization": `Bearer ${token}` },
            });

            const data = await response.json();
            console.log("API Response (Client Data):", data);

            if (!response.ok) {
                throw new Error(data.detail || "Failed to fetch client data.");
            }

            setClientData(data);
        } catch (error) {
            console.error("Fetch error:", error);
            setError("Error fetching client profile.");
        }
    };

    const fetchPlans = async (client_id, token) => {
        try {
            console.log("Fetching repurposed plans...");
            const response = await fetch(`http://localhost:8000/api/repurposed_plans/${client_id}`, {
                method: "GET",
                headers: { "Authorization": `Bearer ${token}` },
            });

            const data = await response.json();
            console.log("API Response (Repurposed Plans):", data);

            if (!response.ok) {
                throw new Error(data.detail || "Failed to fetch repurposed plans.");
            }

            setPlans(data);
        } catch (error) {
            console.error("Fetch error:", error);
            setError("Error fetching repurposed plans.");
        }
    };

    if (error) return <p className="error">{error}</p>;

    return (
        <div className="client-profile-container">
            <h2>Client Profile</h2>
            {clientData ? (
                <div className="client-details">
                    <p><strong>Client ID:</strong> {clientData.client_id}</p>
                    <p><strong>Name:</strong> {clientData.first_name} {clientData.last_name}</p>
                    <p><strong>Email:</strong> {clientData.email}</p>
                    <p><strong>SSN:</strong> {clientData.ssn}</p>
                    <p><strong>Loan Amount:</strong> ${clientData.loan_amount}</p>
                    <p><strong>Delinquencies:</strong> {clientData.delinquencies}</p>
                    <p><strong>Missed Payments:</strong> {clientData.missed_payments}</p>

                    <h3>Repurposed Plans:</h3>
                    {plans.length > 0 ? (
                        <ul>
                            {plans.map((plan, index) => (
                                <li key={index} className="plan-box">
                                    <strong>Plan {plan.plan_number}: {plan.plan_name}</strong>
                                    <p>Loan Adjustment: ${plan.loan_adjustment}</p>
                                    <p>Extension Cycles: {plan.extension_cycles}</p>
                                    <p>Fee Waiver: {plan.fee_waiver}%</p>
                                    <p>Interest Waiver: {plan.interest_waiver}%</p>
                                    <p>Principal Waiver: {plan.principal_waiver}%</p>
                                    <p>Fixed Settlement Amount: ${plan.fixed_settlement}</p>
                                    <p><strong>Description:</strong> {plan.description}</p>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No repurposed plans available for this client.</p>
                    )}
                </div>
            ) : (
                <p>Loading client data...</p>
            )}
        </div>
    );
};

export default ClientProfile;
