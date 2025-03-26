import requests
import json
import os
from typing import List, Dict, Any, Tuple
import time
import dotenv
from together import Together

dotenv.load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")



class LoanNegotiator:
    def __init__(self, model_name="meta-llama/Llama-3.3-70B-Instruct"):
        self.model_name = model_name
        self.conversation_history = []
        self.customer_profile = {}
        self.available_plans = []
        self.current_plan_index = 0
        self.max_retry_attempts = 3
        self.system_prompt = """
        You are an empathetic and professional loan repayment negotiator. Your goal is to help customers 
        who are struggling with loan repayments find a suitable alternative payment plan.
        
        Follow these guidelines:
        1. Always be respectful and understanding of the customer's situation
        2. Present plans clearly with their benefits
        3. Listen to customer concerns and address them specifically
        4. Try to negotiate within the current plan before moving to the next plan
        5. Never make up information about plans not provided to you
        6. Recognize emotional cues in customer responses
        7. Do not agree to terms outside the available plans
        8. If a customer is in severe distress, note the need for human intervention
        
        Your purpose is to find a mutually beneficial solution that helps the customer 
        manage their financial situation while ensuring the loan is eventually repaid.
        """
    
    def set_customer_profile(self, profile: Dict[str, Any]) -> None:
        """
        Set the customer profile with relevant information.
        
        Args:
            profile: Dictionary containing customer information
        """
        self.customer_profile = profile
        print(f"Customer profile set: {profile['name']}")
    
    def set_available_plans(self, plans: List[Dict[str, Any]]) -> None:
        """
        Set the available repayment plans in priority order.
        
        Args:
            plans: List of plan dictionaries, ordered by priority
        """
        self.available_plans = plans
        self.current_plan_index = 0
        print(f"Loaded {len(plans)} payment plans")
    
    def _analyze_sentiment(self, message: str) -> Dict[str, Any]:
        """
        Analyze customer message for sentiment and key concerns.
        
        Args:
            message: Customer's message text
            
        Returns:
            Dictionary with sentiment analysis and detected concerns
        """
        prompt = f"""
        Analyze the following customer message for sentiment and key concerns:
        
        Customer message: "{message}"
        
        Provide a JSON response with the following structure:
        {{
            "sentiment": "positive|negative|neutral",
            "sentiment_score": [number between -1 and 1],
            "primary_concern": "[main issue]",
            "urgency_level": "low|medium|high",
            "willingness_to_negotiate": "low|medium|high",
            "key_mentioned_issues": ["issue1", "issue2"]
        }}
        """
        
        response = self._call_llm(prompt, format_instructions="json")
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback in case of parsing errors
            return {
                "sentiment": "neutral",
                "sentiment_score": 0,
                "primary_concern": "payment difficulty",
                "urgency_level": "medium",
                "willingness_to_negotiate": "medium",
                "key_mentioned_issues": ["payment"]
            }
    
    def _generate_plan_presentation(self, plan: Dict[str, Any]) -> str:
        """
        Generate a presentation of the current plan based on customer profile.
        
        Args:
            plan: The plan details to present
            
        Returns:
            Formatted plan presentation text
        """
        plan_prompt = f"""
        Based on this customer profile:
        - Name: {self.customer_profile.get('name', 'the customer')}
        - Loan amount: ${self.customer_profile.get('loan_amount', 'N/A')}
        - Current monthly payment: ${self.customer_profile.get('current_payment', 'N/A')}
        - Missed payments: {self.customer_profile.get('missed_payments', 'N/A')}
        - Reported reason: {self.customer_profile.get('reported_reason', 'financial difficulty')}
        
        Create a clear, empathetic presentation of this payment plan:
        - Plan name: {plan['name']}
        - New monthly payment: ${plan['monthly_payment']}
        - Term extension: {plan['term_extension']} months
        - Interest adjustment: {plan['interest_adjustment']}
        - Requirements: {', '.join(plan['requirements'])}
        - Key benefits: {', '.join(plan['benefits'])}
        
        Focus on how this plan specifically addresses their situation. Be warm but professional.
        Don't mention other plans unless the customer has already rejected previous options.
        """
        
        return self._call_llm(plan_prompt)
    
    def _generate_negotiation_response(self, customer_message: str, current_plan: Dict[str, Any], 
                                    sentiment_analysis: Dict[str, Any]) -> Tuple[str, bool]:
        """
        Generate a negotiation response based on customer message and sentiment.
        
        Args:
            customer_message: The most recent customer message
            current_plan: The plan currently being negotiated
            sentiment_analysis: Results from sentiment analysis
            
        Returns:
            Tuple of (response text, should_move_to_next_plan)
        """
        # Build context from conversation history (last 3 exchanges)
        recent_context = self.conversation_history[-6:] if len(self.conversation_history) >= 6 else self.conversation_history
        context_str = "\n".join([f"{'Customer' if i%2==0 else 'Negotiator'}: {msg}" 
                              for i, msg in enumerate(recent_context)])
        
        negotiation_prompt = f"""
        Customer profile:
        - Name: {self.customer_profile.get('name', 'the customer')}
        - Loan amount: ${self.customer_profile.get('loan_amount', 'N/A')}
        - Current monthly payment: ${self.customer_profile.get('current_payment', 'N/A')}
        - Missed payments: {self.customer_profile.get('missed_payments', 'N/A')}
        - Reported reason: {self.customer_profile.get('reported_reason', 'financial difficulty')}
        
        Current plan being discussed:
        - Plan name: {current_plan['name']}
        - New monthly payment: ${current_plan['monthly_payment']}
        - Term extension: {current_plan['term_extension']} months
        - Interest adjustment: {current_plan['interest_adjustment']}
        
        Recent conversation:
        {context_str}
        
        Latest customer message: "{customer_message}"
        
        Sentiment analysis:
        - Sentiment: {sentiment_analysis['sentiment']}
        - Primary concern: {sentiment_analysis['primary_concern']}
        - Urgency level: {sentiment_analysis['urgency_level']}
        - Willingness to negotiate: {sentiment_analysis['willingness_to_negotiate']}
        
        Respond to the customer in a way that addresses their specific concerns while trying to reach an 
        agreement on the current plan. If they seem completely unwilling to accept this plan after 
        good-faith negotiation attempts, include the text "[MOVE_TO_NEXT_PLAN]" at the end of your response.
        
        Your response should be empathetic but also firm about what options are actually available.
        """
        
        response = self._call_llm(negotiation_prompt)
        
        # Check if we should move to next plan
        should_move_to_next = "[MOVE_TO_NEXT_PLAN]" in response
        response = response.replace("[MOVE_TO_NEXT_PLAN]", "")
        
        return response.strip(), should_move_to_next
    
    def process_message(self, customer_message: str) -> str:
        """
        Process a customer message and generate appropriate response.
        
        Args:
            customer_message: The customer's message text
            
        Returns:
            Response message from the negotiator
        """
        # Store message in history
        self.conversation_history.append(customer_message)
        
        # Initial message handling
        if len(self.conversation_history) == 1:
            greeting = self._generate_greeting()
            self.conversation_history.append(greeting)
            return greeting
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(customer_message)
        print(f"Sentiment analysis: {sentiment['sentiment']} ({sentiment['sentiment_score']})")
        
        # Get current plan
        if not self.available_plans:
            return "I don't have any payment plans available to discuss. Please contact customer service."
        
        current_plan = self.available_plans[self.current_plan_index]
        
        # Generate response based on conversation stage
        if len(self.conversation_history) == 3:  # After greeting and first customer message
            # Present first plan
            plan_presentation = self._generate_plan_presentation(current_plan)
            self.conversation_history.append(plan_presentation)
            return plan_presentation
        else:
            # We're in negotiation mode
            response, move_to_next = self._generate_negotiation_response(
                customer_message, current_plan, sentiment
            )
            
            # Check if we need to move to next plan
            if move_to_next:
                self.current_plan_index += 1
                if self.current_plan_index < len(self.available_plans):
                    next_plan = self.available_plans[self.current_plan_index]
                    plan_presentation = self._generate_plan_presentation(next_plan)
                    
                    # Combine transition with plan presentation
                    response = f"{response}\n\nI understand this plan doesn't work for your situation. Let me present another option that might be more suitable:\n\n{plan_presentation}"
                else:
                    # We've exhausted all plans
                    response = f"{response}\n\nI understand none of our standard plans seem to fit your situation. I recommend speaking with one of our financial advisors who can create a more customized solution. Would you like me to arrange that for you?"
            
            self.conversation_history.append(response)
            return response
    
    def _generate_greeting(self) -> str:
        """Generate an initial greeting based on customer profile"""
        greeting_prompt = f"""
        Create a warm, professional greeting for a customer who has contacted us about loan repayment difficulties.
        
        Customer details:
        - Name: {self.customer_profile.get('name', 'the customer')}
        - Missed payments: {self.customer_profile.get('missed_payments', 'some')}
        - Reported reason: {self.customer_profile.get('reported_reason', 'financial difficulty')}
        
        Your greeting should:
        1. Welcome them by name
        2. Express understanding about their situation (without being condescending)
        3. Briefly explain that you're here to help find a payment solution
        4. Ask them to share a bit more about their current situation
        
        Keep it concise, empathetic and professional.
        """
        
        return self._call_llm(greeting_prompt)
    
    def _call_llm(self, prompt: str, format_instructions: str = None) -> str:
        """
        Call the LLM API with retry logic.
        
        Args:
            prompt: The prompt to send to the LLM
            format_instructions: Optional format instructions (e.g., "json")
            
        Returns:
            The LLM's response text
        """
        full_prompt = f"{self.system_prompt}\n\n{prompt}"
        
        if format_instructions == "json":
            full_prompt += "\n\nYou must respond with valid JSON only. No explanations or other text."
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "prompt": full_prompt,
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": None
        }
        
        # Add retry logic
        for attempt in range(self.max_retry_attempts):
            try:
                response = requests.post(API_URL, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                
                # Extract text from response based on Together AI's response format
                return result.get("choices", [{}])[0].get("text", "")
                
            except Exception as e:
                print(f"API call attempt {attempt+1} failed: {str(e)}")
                if attempt < self.max_retry_attempts - 1:
                    # Exponential backoff
                    time.sleep(2 ** attempt)
                else:
                    return "I'm having trouble processing your request right now. Please try again in a moment."

# Example usage
if __name__ == "__main__":
    # Initialize negotiator
    negotiator = LoanNegotiator()
    
    # Set customer profile
    customer = {
        "name": "John Smith",
        "loan_amount": 25000,
        "current_payment": 450,
        "missed_payments": 2,
        "reported_reason": "job loss",
        "credit_score": 680,
        "remaining_term": 48
    }
    negotiator.set_customer_profile(customer)
    
    # Define available plans
    plans = [
        {
            "name": "Temporary Reduction Plan",
            "monthly_payment": 225,
            "term_extension": 6,
            "interest_adjustment": "No change",
            "requirements": ["Proof of hardship", "Resume full payments after 6 months"],
            "benefits": ["50% payment reduction", "No impact on credit score", "No additional fees"]
        },
        {
            "name": "Term Extension Plan",
            "monthly_payment": 350,
            "term_extension": 12,
            "interest_adjustment": "No change",
            "requirements": ["One-time processing fee of $50"],
            "benefits": ["Lower monthly payment", "More manageable timeline", "Reduced financial stress"]
        },
        {
            "name": "Interest Relief Plan",
            "monthly_payment": 300,
            "term_extension": 0,
            "interest_adjustment": "Reduced by 2% for 12 months",
            "requirements": ["Auto-payment enrollment", "Financial counseling session"],
            "benefits": ["Interest savings", "More payment goes to principal", "Financial education"]
        }
    ]
    negotiator.set_available_plans(plans)
    
    # Demo conversation
    print("\n--- Conversation Demo ---")
    
    # First customer message
    customer_message = "Hi, I'm having trouble making my loan payments. I lost my job last month."
    print(f"Customer: {customer_message}")
    
    response = negotiator.process_message(customer_message)
    print(f"Negotiator: {response}")
    
    # Second customer message
    customer_message = "I'm not sure I can afford any payments right now. I have some savings but they'll only last a couple months."
    print(f"Customer: {customer_message}")
    
    response = negotiator.process_message(customer_message)
    print(f"Negotiator: {response}")
    
    # Additional exchanges could be added for demonstration