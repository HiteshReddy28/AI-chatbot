export const botResponses = {
    'Can I refinance my existing loan?': 
      "Yes, you can refinance your existing loan...",
    'Does applying for a loan impact my credit score?':
      "Yes, applying for a loan typically results...",
    'How is my financial risk assessed for a loan?':
      "Financial risk assessment involves evaluating...",
    'What are Debt-to-Income (DTI)?':
      "Debt-to-Income (DTI) ratio is a financial measure..."
  };
  
  export const defaultResponse = "I understand your question...";
  
  export const commonPrompts = [
    'Can I refinance my existing loan?',
    'Does applying for a loan impact my credit score?',
    'How is my financial risk assessed for a loan?',
    'What are Debt-to-Income (DTI)?'
  ];
  
  export const chatAPI = {
    sendMessage: async (message) => {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      return response.json();
    }
  };