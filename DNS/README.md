# DNS (Domain Name System)

DNS is like the **address book of the internet**. When you type "google.com" in your browser, DNS finds the actual computer address (IP address) where Google's website lives.

## What Does DNS Actually Do?

Think of DNS like a translator. Computers talk to each other using numbers (like 172.217.3.110), but humans are better at remembering names (like google.com). DNS converts the easy-to-remember names into the numbers that computers need.

## How DNS Is Organized

DNS works like a filing system with different levels:

### Root Servers (The Main Directory)
- These are like the **main phone book** for the entire internet
- There are only 13 groups of these servers worldwide
- They know where to find information about all website endings (.com, .org, etc.)

### Domain Servers (.com, .org servers)
- These handle specific endings like ".com" or ".net"
- They're like **section managers** who know which companies handle which websites
- Called Top-Level Domain (TLD) servers

### Website Servers
- These know the **exact address** for specific websites
- They give you the final IP address you need
- Called authoritative nameservers

## What Happens When You Visit a Website

Here's the simple step-by-step process:

1. **You type** "facebook.com" in your browser
2. **Your computer asks** your internet provider's DNS server "Where is facebook.com?"
3. **DNS server checks** if it already knows (from memory)
4. **If not, it asks** the root servers "Who handles .com websites?"
5. **Root server says** "Ask the .com servers"
6. **DNS server asks** .com servers "Where is facebook.com?"
7. **.com server says** "Ask Facebook's servers"
8. **DNS server asks** Facebook's servers "What's your IP address?"
9. **Facebook's server responds** with their IP address
10. **Your browser connects** to that IP address and loads the website

## Why DNS Matters for System Design

DNS teaches us important lessons:

### It's Spread Out (Distributed)
- No single computer controls all of DNS
- If one server breaks, others keep working
- This makes the internet more reliable

### It Uses Memory (Caching)
- DNS servers remember recent answers
- This makes websites load faster
- Less work for all the servers

### It Can Handle Traffic (Load Balancing)
- Popular websites can have multiple IP addresses
- DNS can send different people to different servers
- This spreads out the load

## Common DNS Records (The Different Types of Information)

Think of DNS records like different types of information in a contact book:

| Type | What It Does | Example |
|------|-------------|---------|
| **A Record** | Basic address | facebook.com → 157.240.3.35 |
| **CNAME** | Nickname/Alias | www.facebook.com → facebook.com |
| **MX Record** | Mail server | Where to send emails for @facebook.com |

## DNS Security Issues

DNS has some problems because it was built when the internet was smaller and more trusted:

### Common Problems
- **Fake Answers** - Bad actors can give wrong IP addresses
- **Eavesdropping** - People can see what websites you're looking up
- **Overloading** - Attackers can flood DNS servers with requests

### Solutions
- **Encrypted DNS** - Hide your DNS requests (like DNS over HTTPS)
- **Secure DNS Services** - Use trusted providers like Google (8.8.8.8) or Cloudflare (1.1.1.1)

## Why This Matters for System Design

Understanding DNS helps you think about building systems that:

- **Don't break easily** - Spread things across multiple servers
- **Work fast** - Remember information you use often
- **Handle lots of users** - Distribute traffic smartly
- **Stay secure** - Don't trust everything, verify important information

## Key Takeaways

DNS is a great example of how to build something that:
- Serves billions of people every day
- Rarely breaks down
- Gets faster over time through smart caching
- Can grow without falling apart

