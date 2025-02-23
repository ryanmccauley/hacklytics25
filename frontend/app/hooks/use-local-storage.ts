import { useEffect, useState } from "react"

export function useLocalStorage<T>(
	key: string,
	initialValue: T,
): [T, (value: T) => void] {
	if (typeof window === "undefined") {
		return [initialValue, () => {}]
	}

	const [value, setValue] = useState<T>(() => {
		const item = localStorage.getItem(key)
		return item ? JSON.parse(item) : initialValue
	})

	useEffect(() => {
		localStorage.setItem(key, JSON.stringify(value))
	}, [value])

	return [value, setValue]
}
