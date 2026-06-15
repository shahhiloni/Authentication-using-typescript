# AI Boyfriend Chatbot

A React + Next.js + TypeScript starter for a personal companion chatbot. The app runs in the browser, remembers the user's name during the session, detects a few simple moods, and responds with warm preset messages.

> Note: This is a starter project, not a replacement for real human support or professional mental health care.

## Tech stack

- React
- Next.js App Router
- TypeScript
- CSS modules via `app/globals.css`

## Requirements

- Node.js 18.18 or newer
- npm

## Install

```bash
npm install
```

## Run locally

```bash
npm run dev
```

Open <http://localhost:3000> in your browser.

## Build

```bash
npm run build
npm start
```

## Example things to type

- `my name is Alex`
- `I feel tired today`
- `I am anxious about tomorrow`
- `what is your name?`
- `give me a date idea`
- `help`

## Customize the boyfriend personality

Edit `app/page.tsx` and change:

- `botName` for the chatbot's name
- `moodKeywords` for emotion detection
- `createMoodReply` for the response style
- `createReply` for new commands and behaviors

Edit `app/globals.css` to change the colors, spacing, and chat bubble design.
