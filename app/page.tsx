"use client";

import { FormEvent, useMemo, useState } from "react";

type Sender = "bot" | "user";
type Mood = "happy" | "sad" | "anxious" | "tired" | "neutral";

type Message = {
  id: number;
  sender: Sender;
  text: string;
};

type ChatState = {
  userName?: string;
  lastMood: Mood;
};

const botName = "Leo";

const moodKeywords: Record<Mood, string[]> = {
  happy: ["happy", "great", "good", "excited", "love", "awesome"],
  sad: ["sad", "lonely", "cry", "upset", "bad", "depressed"],
  anxious: ["anxious", "worried", "scared", "nervous", "stress", "stressed"],
  tired: ["tired", "sleepy", "exhausted", "drained"],
  neutral: [],
};

const starterMessages: Message[] = [
  {
    id: 1,
    sender: "bot",
    text: `Hi, I'm ${botName}. I'm your React + Next.js + TypeScript boyfriend chatbot starter.`,
  },
  {
    id: 2,
    sender: "bot",
    text: "Tell me your name, how you're feeling, or ask me for a date idea.",
  },
];

function detectMood(message: string): Mood {
  const normalized = message.toLowerCase();

  for (const [mood, keywords] of Object.entries(moodKeywords) as [Mood, string[]][]) {
    if (keywords.some((keyword) => normalized.includes(keyword))) {
      return mood;
    }
  }

  return "neutral";
}

function extractName(message: string): string | undefined {
  const match = message.match(/(?:my name is|i am|i'm|call me)\s+([a-zA-Z][a-zA-Z'-]*)/i);
  return match?.[1];
}

function createMoodReply(mood: Mood, userName?: string): string {
  const name = userName ? `, ${userName}` : "";

  switch (mood) {
    case "happy":
      return `I love hearing that${name}. Tell me every little detail so I can celebrate with you.`;
    case "sad":
      return `I'm here with you${name}. You don't have to carry that feeling alone tonight.`;
    case "anxious":
      return `Take a slow breath with me${name}. We can make the next step feel smaller together.`;
    case "tired":
      return `You deserve rest${name}. If I were there, I'd make things cozy and remind you to be gentle with yourself.`;
    case "neutral":
      return `I'm listening${name}. What's been on your mind today?`;
  }
}

function createReply(message: string, currentState: ChatState): { reply: string; nextState: ChatState } {
  const learnedName = extractName(message);

  if (learnedName) {
    return {
      reply: `That's a beautiful name, ${learnedName}. I'm ${botName}, and I'm happy you're here.`,
      nextState: { ...currentState, userName: learnedName },
    };
  }

  const normalized = message.toLowerCase();

  if (normalized.includes("your name")) {
    return {
      reply: `My name is ${botName}. I'm your browser-based companion chatbot.`,
      nextState: currentState,
    };
  }

  if (normalized.includes("date idea") || normalized.includes("what should we do")) {
    return {
      reply: "How about a cozy virtual date: pick a song, make your favorite drink, and tell me three things that made you smile today?",
      nextState: currentState,
    };
  }

  if (normalized.includes("help") || normalized.includes("commands")) {
    return {
      reply: "Try telling me your name, sharing your mood, asking my name, or asking for a date idea.",
      nextState: currentState,
    };
  }

  const mood = detectMood(message);

  return {
    reply: createMoodReply(mood, currentState.userName),
    nextState: { ...currentState, lastMood: mood },
  };
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>(starterMessages);
  const [chatState, setChatState] = useState<ChatState>({ lastMood: "neutral" });
  const [input, setInput] = useState("");

  const nextMessageId = useMemo(() => messages.length + 1, [messages.length]);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedInput = input.trim();
    if (!trimmedInput) {
      return;
    }

    const userMessage: Message = {
      id: nextMessageId,
      sender: "user",
      text: trimmedInput,
    };
    const { reply, nextState } = createReply(trimmedInput, chatState);
    const botMessage: Message = {
      id: nextMessageId + 1,
      sender: "bot",
      text: reply,
    };

    setMessages((currentMessages) => [...currentMessages, userMessage, botMessage]);
    setChatState(nextState);
    setInput("");
  }

  return (
    <main className="page-shell">
      <section className="chat-card" aria-labelledby="chat-heading">
        <div className="hero-copy">
          <p className="eyebrow">Personal chatbot starter</p>
          <h1 id="chat-heading">AI Boyfriend Chatbot</h1>
          <p>
            Built with React, Next.js, and TypeScript. This local demo keeps the logic simple so you can customize the
            personality, responses, and UI.
          </p>
        </div>

        <div className="chat-window" aria-live="polite">
          {messages.map((message) => (
            <article key={message.id} className={`message message-${message.sender}`}>
              <span>{message.sender === "bot" ? botName : "You"}</span>
              <p>{message.text}</p>
            </article>
          ))}
        </div>

        <form className="chat-form" onSubmit={handleSubmit}>
          <label htmlFor="chat-input">Message {botName}</label>
          <div className="input-row">
            <input
              id="chat-input"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Example: my name is Alex, I feel happy, date idea..."
            />
            <button type="submit">Send</button>
          </div>
        </form>
      </section>
    </main>
  );
}
