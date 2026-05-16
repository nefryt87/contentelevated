import { NextResponse } from "next/server";

export async function POST(request) {
  const { email } = await request.json().catch(() => ({}));
  const formId = process.env.KIT_FORM_ID || process.env.CONVERTKIT_FORM_ID;
  const apiKey = process.env.KIT_API_KEY || process.env.CONVERTKIT_API_KEY;

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return NextResponse.json({ error: "Enter a valid email address." }, { status: 400 });
  }

  if (!formId || !apiKey) {
    return NextResponse.json({ error: "Newsletter is not configured yet." }, { status: 500 });
  }

  const response = await fetch(`https://api.convertkit.com/v3/forms/${formId}/subscribe`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: apiKey,
      email
    })
  });

  if (!response.ok) {
    return NextResponse.json({ error: "Signup failed. Please try again." }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}
