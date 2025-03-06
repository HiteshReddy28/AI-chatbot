import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ClientProfile.css";

const ClientProfile = () => {
    const navigate = useNavigate();
    const [clientData, setClientData] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        const token = localStorage.getItem("token");
        let client_id = localStorage.getItem("client_id");

        console.log("LocalStorage Token:", token);  //debug
        console.log("LocalStorage Client ID:", client_id);

        if (!token) {
            alert("You must be logged in to view your profile.");
            navigate("/login");
            return;
        }

        // ✅ Fetch client_id from backend if missing
        if (!client_id) {
            fetch(`http://localhost:8000/api/userinfo`, {
                method: "GET",
                headers: { "Authorization": `Bearer ${token}` },
            })
            .then(response => response.json())
            .then(data => {
                console.log("Fetched client_id from API:", data.client_id);
                if (data.client_id) {
                    localStorage.setItem("client_id", data.client_id);
                    client_id = data.client_id;  //Update client_id
                    fetchClientData(data.client_id, token);
                } else {
                    alert("Failed to retrieve client information.");
                    navigate("/login");
                }
            })
            .catch(error => console.error("Error fetching client_id:", error));
        } else {
            fetchClientData(client_id, token);
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
            console.log("API Response:", data);

            if (!response.ok) {
                throw new Error(data.detail || "Failed to fetch client data.");
            }

            setClientData(data);
        } catch (error) {
            console.error("Fetch error:", error);
            setError("Error fetching client profile.");
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

                    <h3>Repurposed Plans:</h3>
                    <ul>
                        {clientData.repurposed_plans.map((plan, index) => (
                            <li key={index} className="plan-box">
                                <strong>Plan {plan.plan_number}</strong>
                                <p>Loan Adjustment: ${plan.loan_adjustment}</p>
                                <p>Extension Cycles: {plan.extension_cycles}</p>
                                <p>Fee Waiver: {plan.fee_waiver}%</p>
                                <p>Interest Waiver: {plan.interest_waiver}%</p>
                                <p>Principal Waiver: {plan.principal_waiver}%</p>
                                <p>Fixed Settlement Amount: ${plan.fixed_settlement}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>Loading client data...</p>
            )}
        </div>
    );
};

export default ClientProfile;
