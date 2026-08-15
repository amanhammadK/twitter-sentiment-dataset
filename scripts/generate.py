import json, random, os, math
from pathlib import Path
from datetime import datetime, timedelta

HERE = Path(__file__).parent
DATA_DIR = HERE.parent / "data"

def gen_twitter(n=2000):
    random.seed(42)
    hashtags = ["#AI", "#MachineLearning", "#Python", "#Tech", "#DataScience",
                "#Innovation", "#Startup", "#Crypto", "#Web3", "#Climate",
                "#Politics", "#Sports", "#Music", "#Food", "#Travel",
                "#Health", "#Fitness", "#Fashion", "#Gaming", "#Movies"]
    hashtag_popularity = [0.15, 0.12, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04,
                          0.04, 0.03, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.01]
    hashtag_pairs = {("#AI", "#MachineLearning"): 0.3, ("#Tech", "#Innovation"): 0.25,
                     ("#Crypto", "#Web3"): 0.4, ("#Startup", "#Tech"): 0.3,
                     ("#Health", "#Fitness"): 0.35, ("#Food", "#Travel"): 0.2}
    brands = ["Apple", "Google", "Microsoft", "Amazon", "Tesla", "Meta", "Netflix",
              "Spotify", "OpenAI", "Samsung", "Nike", "Adidas", "CocaCola", "Pepsi"]
    brand_sentiment_bias = {"Tesla": -0.1, "OpenAI": 0.15, "Apple": 0.05, "Meta": -0.15}
    usernames = [f"user_{random.randint(1000,9999)}" for _ in range(200)]
    influencer_probs = [0.05] * 20 + [0.95] * 180
    emojis_positive = ["", "🔥", "❤️", "👍", "🎉", "💯", "✨", "🙌", "💪", "🚀"]
    emojis_negative = ["", "😡", "👎", "😤", "💔", "🙄", "😴", "🤦", "😒", "😠"]
    emojis_neutral = ["", "🤔", "👀", "📊", "📰", "💬", "🔗", "📌", "🔍", "📝"]
    positive_templates = [
        "Just got the new {brand} product and it's amazing! {hashtag} {emoji}",
        "Love the latest update from {brand}. Great work! {hashtag} {emoji}",
        "{brand} really delivered this time. Highly recommend! {hashtag} {emoji}",
        "Best purchase I've made this year. Thanks {brand}! {hashtag} {emoji}",
        "The {brand} team is killing it. Keep it up! {hashtag} {emoji}",
        "Switched to {brand} and couldn't be happier. {hashtag} {emoji}",
        "{brand} customer service was excellent today. {hashtag} {emoji}",
        "Finally tried {brand}'s new feature. It's a game changer! {hashtag} {emoji}"
    ]
    negative_templates = [
        "Disappointed with {brand}'s latest release. Expected better. {hashtag} {emoji}",
        "{brand}'s customer support is terrible. Still waiting. {hashtag} {emoji}",
        "The new {brand} update broke everything. Fix this! {hashtag} {emoji}",
        "Regarding my {brand} purchase - worst decision ever. {hashtag} {emoji}",
        "{brand} needs to step up their game. Competitors are better. {hashtag} {emoji}",
        "Can't believe {brand} charged me for this. Scam. {hashtag} {emoji}",
        "Another {brand} outage? Unacceptable. {hashtag} {emoji}",
        "{brand}'s quality has gone downhill lately. {hashtag} {emoji}"
    ]
    neutral_templates = [
        "Just saw the {brand} announcement. Interesting moves. {hashtag} {emoji}",
        "Comparing {brand} with competitors. Thoughts? {hashtag} {emoji}",
        "{brand} stock is steady today. Market seems uncertain. {hashtag} {emoji}",
        "Reading about {brand}'s latest quarterly results. {hashtag} {emoji}",
        "The {brand} vs {brand2} debate continues. {hashtag} {emoji}",
        "Anyone else following {brand}'s expansion plans? {hashtag} {emoji}",
        "{brand} released their annual report. Numbers are mixed. {hashtag} {emoji}",
        "Hot take: {brand} is overrated but not terrible. {hashtag} {emoji}"
    ]
    sentiments = ["positive", "negative", "neutral"]
    weights = [0.4, 0.3, 0.3]
    out = []
    base_time = datetime(2024, 1, 1)
    influencer_flags = random.choices([True, False], weights=influencer_probs, k=200)
    for i in range(n):
        sentiment = random.choices(sentiments, weights=weights, k=1)[0]
        brand = random.choice(brands)
        brand2 = random.choice([b for b in brands if b != brand])
        sentiment_modifier = brand_sentiment_bias.get(brand, 0)
        if random.random() < abs(sentiment_modifier):
            sentiment = "positive" if sentiment_modifier > 0 else "negative"
        primary_hashtag = random.choices(hashtags, weights=hashtag_popularity, k=1)[0]
        secondary_hashtags = []
        if random.random() < 0.35:
            for pair, prob in hashtag_pairs.items():
                if primary_hashtag in pair and random.random() < prob:
                    other = [h for h in pair if h != primary_hashtag][0]
                    secondary_hashtags.append(other)
        if random.random() < 0.2 and not secondary_hashtags:
            secondary_hashtags.append(random.choice(hashtags))
        all_hashtags = [primary_hashtag] + secondary_hashtags[:2]
        if sentiment == "positive":
            emoji = random.choice(emojis_positive)
            text = random.choice(positive_templates).format(brand=brand, hashtag=primary_hashtag, emoji=emoji)
        elif sentiment == "negative":
            emoji = random.choice(emojis_negative)
            text = random.choice(negative_templates).format(brand=brand, hashtag=primary_hashtag, emoji=emoji)
        else:
            emoji = random.choice(emojis_neutral)
            text = random.choice(neutral_templates).format(brand=brand, brand2=brand2, hashtag=primary_hashtag, emoji=emoji)
        hour = random.choices(range(24),
            weights=[1,1,1,1,1,2,4,7,8,7,5,4,5,6,7,8,7,6,5,4,3,2,1,1], k=1)[0]
        tweet_time = base_time + timedelta(
            days=random.randint(0, 365),
            hours=hour,
            minutes=random.randint(0, 59)
        )
        is_influencer = random.choice(influencer_flags)
        base_likes = random.lognormvariate(3, 2) if not is_influencer else random.lognormvariate(5, 1.5)
        base_retweets = base_likes * random.uniform(0.1, 0.3)
        base_replies = base_likes * random.uniform(0.05, 0.15)
        sentiment_engagement = {"positive": 1.2, "negative": 1.5, "neutral": 0.8}
        engagement_mult = sentiment_engagement[sentiment]
        likes = max(0, int(base_likes * engagement_mult * random.uniform(0.5, 1.5)))
        retweets = max(0, int(base_retweets * engagement_mult * random.uniform(0.5, 1.5)))
        replies = max(0, int(base_replies * engagement_mult * random.uniform(0.5, 1.5)))
        if random.random() < 0.05:
            likes *= random.randint(5, 50)
            retweets *= random.randint(3, 20)
        confidence_base = 0.75 if sentiment != "neutral" else 0.65
        confidence = round(min(0.99, max(0.5, random.gauss(confidence_base, 0.08))), 2)
        out.append({
            "id": f"tw_{i:06d}",
            "text": text,
            "sentiment": sentiment,
            "confidence": confidence,
            "username": random.choice(usernames),
            "timestamp": tweet_time.isoformat(),
            "likes": min(likes, 500000),
            "retweets": min(retweets, 100000),
            "replies": min(replies, 50000),
            "hashtags": all_hashtags,
            "brand": brand,
            "verified": is_influencer and random.random() < 0.4,
            "emoji_count": len(emoji),
            "text_length": len(text),
            "hour_of_day": tweet_time.hour,
            "day_of_week": tweet_time.strftime("%A"),
            "is_thread": random.random() < 0.08,
            "has_media": random.random() < 0.25,
            "has_url": random.random() < 0.3,
            "follower_count": int(random.lognormvariate(6, 2)) if is_influencer else int(random.lognormvariate(3, 1.5)),
        })
    return out

def main():
    data = gen_twitter()
    DATA_DIR.mkdir(exist_ok=True)
    out = DATA_DIR / "dataset.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Generated {len(data)} twitter sentiment records")
    print(f"Saved to {out}")

if __name__ == "__main__":
    main()
