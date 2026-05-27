import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST(request) {
  const { email } = await request.json().catch(() => ({}));
  const formId = process.env.KIT_FORM_ID || process.env.CONVERTKIT_FORM_ID;
  const apiKey = process.env.KIT_API_KEY || process.env.CONVERTKIT_API_KEY;
  const apiVersion = (process.env.KIT_API_VERSION || "v4").toLowerCase();
  const cleanEmail = typeof email === "string" ? email.trim().toLowerCase() : "";

  if (!cleanEmail || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleanEmail)) {
    return NextResponse.json({ error: "Enter a valid email address." }, { status: 400 });
  }

  if (!formId || !apiKey) {
    return NextResponse.json({ error: "Newsletter is not configured yet." }, { status: 500 });
  }

  const response = apiVersion === "v3"
    ? await subscribeWithLegacyKit(formId, apiKey, cleanEmail)
    : await subscribeWithKitV4(formId, apiKey, cleanEmail);

  if (!response.ok) {
    return NextResponse.json({ error: "Signup failed. Please try again." }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}

async function subscribeWithLegacyKit(formId, apiKey, email) {
  return fetch(`https://api.convertkit.com/v3/forms/${formId}/subscribe`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: apiKey,
      email
    })
  });
}

async function subscribeWithKitV4(formId, apiKey, email) {
  const headers = {
    "Content-Type": "application/json",
    "X-Kit-Api-Key": apiKey
  };

  const subscriberResponse = await fetch("https://api.kit.com/v4/subscribers", {
    method: "POST",
    headers,
    body: JSON.stringify({ email_address: email })
  });

  if (!subscriberResponse.ok && subscriberResponse.status !== 409) {
    return subscriberResponse;
  }

  return fetch(`https://api.kit.com/v4/forms/${formId}/subscribers`, {
    method: "POST",
    headers,
    body: JSON.stringify({ email_address: email })
  });
}
